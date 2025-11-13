from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from datetime import datetime
import json
import ast

from extensions import db
from schemas.bulk_users import BulkUserDataSchema
from routes.bulk_add import ensure_category, ensure_subcategory, ensure_product
from models.registration import User, CustomerProfile, Address
from models.analytics import UserSession, ProductView
from models.shopping import Order, OrderItem
from models.catalog import Product, Review

bulk_users_bp = Blueprint("bulk_users", __name__, url_prefix="/bulk/users")


# --------------------------
# Helpers
# --------------------------

def _parse_iso_dt(value: str) -> datetime:
    if not value:
        return datetime.utcnow()
    try:
        if value.endswith("Z"):
            # Convert Z (UTC) to +00:00 for fromisoformat
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except Exception:
        # Try date only
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return datetime.utcnow()


def _load_payload_tolerant() -> dict:
    """Load JSON normally; if not JSON, try to strip JS export wrappers.
    Supports bodies like `export const userData = {...};` or `module.exports = {...}`.
    """
    data = request.get_json(silent=True)
    if data:
        return data

    raw = request.get_data(as_text=True) or ""
    text = raw.strip()
    if not text:
        return {}

    # Strip common wrappers
    prefixes = [
        "export const userData =",
        "export default",
        "module.exports =",
        "exports.userData =",
    ]
    for p in prefixes:
        if text.startswith(p):
            text = text[len(p):].strip()
            break

    # Remove trailing semicolon if present
    if text.endswith(";"):
        text = text[:-1].strip()

    # Try JSON first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Fallback to Python-literal parser (safer than eval)
    try:
        return ast.literal_eval(text)
    except Exception:
        return {}


# --------------------------
# Core ingestion
# --------------------------
@bulk_users_bp.route("", methods=["POST"])
def ingest_user_data():
    """Bulk ingest user analytics dataset.

    Steps:
    - Validate dataset
    - Upsert products (flat list) into catalog (category/subcategory created as needed)
    - Upsert users with basic profile/address
    - Create sessions and product views
    - Create orders+items from purchases and attach reviews
    - Create views from search result clicks to enrich engagement signals
    """
    payload = _load_payload_tolerant()
    if not payload:
        return jsonify({"error": "validation_error", "message": "Empty or invalid payload"}), 400

    try:
        data = BulkUserDataSchema().load(payload)
    except Exception as e:
        return jsonify({"error": "validation_error", "message": str(e)}), 400

    # Maps from external ids to DB ids
    sample_prod_to_db: dict[int, int] = {}
    created_counts = {
        "products": 0, "users": 0, "sessions": 0, "views": 0, "orders": 0, "order_items": 0, "reviews": 0
    }
    updated_counts = {
        "products": 0, "users": 0
    }

    try:
        # 1) Upsert products referenced in dataset
        for p in data.get("products", []):
            cat_name = p["category_info"]["main_category"]
            sub_name = p["category_info"]["subcategory"]
            category, _ = ensure_category(cat_name)
            subcat, _ = ensure_subcategory(category, sub_name)
            # Map to ensure_product expected fields
            prod_payload = {
                "name": p["name"],
                "description": p.get("description") or "",
                "price": float(p.get("price") or 0.0),
                "tags": p.get("tags") or [],
                # no images in this dataset
            }
            existing = db.session.execute(
                select(Product).filter_by(
                    name=p["name"], subcategory_id=subcat.id)
            ).scalar_one_or_none()
            product, created = ensure_product(subcat, prod_payload)
            sample_prod_to_db[p["id"]] = product.id
            if created:
                created_counts["products"] += 1
            else:
                updated_counts["products"] += 1

        # 2) Upsert users (basic info); synthesize email/password
        for u in data.get("users", []):
            synthetic_email = f"user{u['user_id']}@example.com"
            user = db.session.execute(select(User).filter_by(
                email=synthetic_email)).scalar_one_or_none()
            if not user:
                user = User(
                    email=synthetic_email,
                    password_hash=generate_password_hash("Password123!"),
                )
                # created_at if provided
                if u.get("created_at"):
                    try:
                        user.created_at = datetime.fromisoformat(
                            u["created_at"])  # date-only accepted
                    except Exception:
                        pass
                db.session.add(user)
                db.session.flush()
                created_counts["users"] += 1
            else:
                updated_counts["users"] += 1

            # Minimal customer profile
            if not user.customer_profile:
                profile = CustomerProfile(
                    user_id=user.id, first_name=f"User{u['user_id']}", last_name="Sample")
                db.session.add(profile)

            # Minimal address from location
            if (u.get("location")):
                addr = Address(
                    user_id=user.id,
                    line1="Unknown",
                    city=u["location"],
                    state="N/A",
                    zip_code="00000",
                    country="USA",
                )
                db.session.add(addr)

        # 3) Sessions and product views
        for s in data.get("sessions", []):
            user = db.session.execute(select(User).filter_by(
                email=f"user{s['user_id']}@example.com")).scalar_one_or_none()
            if not user:
                continue
            sess = UserSession(
                user_id=user.id,
                ip_address="127.0.0.1",
                user_agent="bulk-import",
                session_start=_parse_iso_dt(s.get("session_start")),
                session_end=_parse_iso_dt(s.get("session_end")),
                pages_visited=len(s.get("products_viewed") or []),
            )
            db.session.add(sess)
            db.session.flush()
            created_counts["sessions"] += 1

            pv_ids = s.get("products_viewed") or []
            durations = s.get("view_durations") or []
            for idx, ext_pid in enumerate(pv_ids):
                db_pid = sample_prod_to_db.get(ext_pid)
                if not db_pid:
                    continue
                view_time = int(durations[idx]) if idx < len(durations) else 0
                pv = ProductView(
                    product_id=db_pid,
                    user_id=user.id,
                    session_id=sess.id,
                    view_time=view_time,
                    viewed_at=sess.session_start,
                    added_to_cart=False,
                )
                db.session.add(pv)
                created_counts["views"] += 1

        # 4) Interactions -> views/add_to_cart/ratings (skip purchases here; handled below)
        for it in data.get("interactions", []):
            user = db.session.execute(select(User).filter_by(
                email=f"user{it['user_id']}@example.com")).scalar_one_or_none()
            if not user:
                continue
            db_pid = sample_prod_to_db.get(it["product_id"]) if it.get(
                "product_id") is not None else None
            if it["interaction_type"] == "view" and db_pid:
                pv = ProductView(
                    product_id=db_pid,
                    user_id=user.id,
                    session_id=None,
                    view_time=int(it.get("duration_seconds") or 0),
                    viewed_at=_parse_iso_dt(it.get("timestamp")),
                    added_to_cart=False,
                )
                db.session.add(pv)
                created_counts["views"] += 1
            elif it["interaction_type"] == "add_to_cart" and db_pid:
                pv = ProductView(
                    product_id=db_pid,
                    user_id=user.id,
                    session_id=None,
                    view_time=0,
                    viewed_at=_parse_iso_dt(it.get("timestamp")),
                    added_to_cart=True,
                )
                db.session.add(pv)
                created_counts["views"] += 1
            elif it["interaction_type"] == "rating" and db_pid:
                # Upsert review for (user, product)
                existing = db.session.execute(
                    select(Review).filter_by(
                        product_id=db_pid, user_id=user.id)
                ).scalar_one_or_none()
                rating_val = float(it.get("rating_given") or 0.0)
                if existing:
                    existing.rating = rating_val
                else:
                    rv = Review(
                        product_id=db_pid,
                        user_id=user.id,
                        rating=rating_val,
                        title="Rating",
                        comment=None,
                        created_on=_parse_iso_dt(it.get("timestamp")),
                    )
                    db.session.add(rv)
                    created_counts["reviews"] += 1
            # 'purchase' in interactions is ignored to prevent duplication

        # 5) Purchases -> create Order and OrderItem, attach review
        for p in data.get("purchases", []):
            user = db.session.execute(select(User).filter_by(
                email=f"user{p['user_id']}@example.com")).scalar_one_or_none()
            if not user:
                continue
            db_pid = sample_prod_to_db.get(p["product_id"]) if p.get(
                "product_id") is not None else None
            if not db_pid:
                continue

            qty = int(p.get("quantity") or 1)
            price_paid = float(p.get("price_paid") or 0.0)
            subtotal = price_paid  # already total paid for line according to dataset
            tax_total = 0.0
            total = subtotal + tax_total

            order = Order(
                user_id=user.id,
                status="completed",
                subtotal=subtotal,
                tax_total=tax_total,
                total=total,
                placed_at=_parse_iso_dt(p.get("purchase_date")),
            )
            db.session.add(order)
            db.session.flush()
            created_counts["orders"] += 1

            item = OrderItem(
                order_id=order.id,
                product_id=db_pid,
                quantity=qty,
                price_per_unit=(price_paid / qty) if qty else price_paid,
            )
            db.session.add(item)
            created_counts["order_items"] += 1

            # Optional review from purchase
            if p.get("rating_given") is not None:
                existing = db.session.execute(
                    select(Review).filter_by(
                        product_id=db_pid, user_id=user.id)
                ).scalar_one_or_none()
                if existing:
                    existing.rating = float(p.get("rating_given"))
                    # Do not overwrite comment if already present from interactions
                    if not existing.comment and p.get("review_text"):
                        existing.comment = p.get("review_text")
                else:
                    rv = Review(
                        product_id=db_pid,
                        user_id=user.id,
                        rating=float(p.get("rating_given")),
                        title="Review",
                        comment=p.get("review_text"),
                        created_on=_parse_iso_dt(p.get("purchase_date")),
                    )
                    db.session.add(rv)
                    created_counts["reviews"] += 1

        # 6) Search queries -> record result clicks as lightweight views
        for q in data.get("search_queries", []):
            user = db.session.execute(select(User).filter_by(
                email=f"user{q['user_id']}@example.com")).scalar_one_or_none()
            if not user:
                continue
            ts = _parse_iso_dt(q.get("timestamp"))
            for ext_pid in (q.get("results_clicked") or []):
                db_pid = sample_prod_to_db.get(ext_pid)
                if not db_pid:
                    continue
                pv = ProductView(
                    product_id=db_pid,
                    user_id=user.id,
                    session_id=None,
                    view_time=0,
                    viewed_at=ts,
                    added_to_cart=False,
                )
                db.session.add(pv)
                created_counts["views"] += 1

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "integrity_error", "message": str(e.orig)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "server_error", "message": str(e)}), 500

    return jsonify({
        "status": "ok",
        "created": created_counts,
        "updated": updated_counts,
        "mapped_products": len(sample_prod_to_db)
    }), 200
