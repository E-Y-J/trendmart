from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from extensions import db
from schemas.bulk_add import BulkAddSchema
from models.catalog import Category, Subcategory, Product
from ai_recom_system.helpers.slugify import slugify

bulk_bp = Blueprint("bulk", __name__, url_prefix="/api/bulk")


def ensure_category(name: str) -> tuple[Category, bool]:
    '''Ensure a category exists by name. Returns (category, created).'''
    slug = slugify(name)
    category = db.session.execute(
        select(Category).filter_by(slug=slug)
    ).scalar_one_or_none()
    if category:
        if category.name != name:
            category.name = name
        return category, False

    category = Category(name=name, slug=slug)
    db.session.add(category)
    db.session.flush()  # assign id
    return category, True


def ensure_subcategory(category: Category, name: str) -> tuple[Subcategory, bool]:
    '''Ensure a subcategory exists under the given category by name. Returns (subcategory, created).'''
    # globally unique by prefixing category slug
    sub_slug = slugify(f"{category.slug}-{name}")
    subcat = db.session.execute(
        select(Subcategory).filter_by(slug=sub_slug)
    ).scalar_one_or_none()
    if subcat:
        changed = False
        if subcat.name != name:
            subcat.name = name
            changed = True
        if subcat.category_id != category.id:
            subcat.category_id = category.id
            changed = True
        return subcat, False

    subcat = Subcategory(name=name, slug=sub_slug, category_id=category.id)
    db.session.add(subcat)
    db.session.flush()
    return subcat, True


def _normalize_tags_csv(tags) -> str | None:
    ''' Normalize tags input into a comma-separated string.'''
    if not tags:
        return None
    if isinstance(tags, str):
        items = [t.strip() for t in tags.split(",") if t.strip()]
    else:
        items = [str(t).strip() for t in tags if t and str(t).strip()]
    return ",".join(items) if items else None


def _pick_image(p: dict) -> str | None:
    '''Pick the best available image URL from the product dict.
    Preference order: image_url > image_thumb_url > primary_image
    '''
    return p.get("image_url") or p.get("image_thumb_url") or p.get("primary_image")


def _unique_sku(base: str) -> str:
    """
    Return a unique SKU by checking and appending -1..-10 if needed.
    Avoids IntegrityError/rollback by deciding before insert.
    """
    base = slugify(base)
    if not db.session.execute(select(Product.id).filter_by(sku=base)).first():
        return base
    for i in range(1, 11):
        candidate = f"{base}-{i}"
        if not db.session.execute(select(Product.id).filter_by(sku=candidate)).first():
            return candidate
    # last resort - still deterministic but very unlikely to hit
    return f"{base}-x"


def ensure_product(subcat: Subcategory, p: dict) -> tuple[Product, bool]:
    """
    Returns (product, created)
    Match priority: incoming SKU -> (name + subcategory)
    """
    name = (p.get("name") or "").strip()
    assert name, "Product name required"

    incoming_sku = (p.get("sku") or "").strip()
    product = None
    if incoming_sku:
        product = db.session.execute(
            select(Product).filter_by(sku=incoming_sku)
        ).scalar_one_or_none()

    if not product:
        product = db.session.execute(
            select(Product).filter_by(name=name, subcategory_id=subcat.id)
        ).scalar_one_or_none()

    tags_csv = _normalize_tags_csv(p.get("tags"))
    image = _pick_image(p)
    price = float(p.get("price") or 0.0)
    desc = p.get("description") or ""

    if product:
        # update in-place
        product.name = name
        product.description = desc
        product.price = price
        if tags_csv is not None:
            product.tags = tags_csv
        if image:
            product.product_img = image
        if product.subcategory_id != subcat.id:
            product.subcategory_id = subcat.id
        return product, False

    # create new product with unique SKU
    base_sku = incoming_sku or slugify(f"{subcat.slug}-{name}")
    sku = _unique_sku(base_sku)
    product = Product(
        sku=sku,
        name=name,
        description=desc,
        price=price,
        product_img=image,
        tags=tags_csv,
        subcategory_id=subcat.id,
    )
    db.session.add(product)
    db.session.flush()
    return product, True


@bulk_bp.route("/add", methods=["POST"])
def bulk_add():
    """
    Ingest a nested structure of categories -> subcategories -> products.
    Body is validated by BulkAddSchema (validation-only Marshmallow schemas).
    """
    payload = request.get_json(silent=True) or {}
    try:
        data = BulkAddSchema().load(payload)
    except Exception as e:
        return jsonify({"error": "validation_error", "message": str(e)}), 400

    created = {"categories": 0, "subcategories": 0, "products": 0}
    updated = {"categories": 0, "subcategories": 0, "products": 0}
    results = {"categories": []}

    try:
        # Process each category
        for cat in data.get("categories", []):
            cat_name = cat["main_category"]

            existing_cat = db.session.execute(
                select(Category.id).filter_by(slug=slugify(cat_name))
            ).first()
            category, cat_created = ensure_category(cat_name)
            created["categories"] += int(cat_created)
            updated["categories"] += int(bool(existing_cat)
                                         and not cat_created)

            cat_out = {"name": category.name,
                       "id": category.id, "subcategories": []}

            # Process each subcategory
            for sub in cat.get("subcategories", []):
                sub_name = sub["name"]

                existing_sub = db.session.execute(
                    select(Subcategory.id).filter_by(
                        slug=slugify(f"{category.slug}-{sub_name}")
                    )
                ).first()
                # Ensure subcategory exists
                subcat, sub_created = ensure_subcategory(category, sub_name)
                created["subcategories"] += int(sub_created)
                updated["subcategories"] += int(bool(existing_sub)
                                                and not sub_created)
                # Prepare output structure
                sub_out = {"name": subcat.name,
                           "id": subcat.id, "products": []}
                # Process each product
                for p in sub.get("products", []):
                    product, prod_created = ensure_product(subcat, p)
                    created["products"] += int(prod_created)
                    updated["products"] += int(not prod_created)

                    sub_out["products"].append(
                        {"id": product.id, "sku": product.sku, "name": product.name}
                    )

                cat_out["subcategories"].append(sub_out)

            results["categories"].append(cat_out)

        db.session.commit()
    except IntegrityError as e:  # likely SKU conflict
        db.session.rollback()
        return jsonify({"error": "integrity_error", "message": str(e.orig)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "server_error", "message": str(e)}), 500

    return jsonify({"status": "ok", "created": created, "updated": updated, "results": results}), 200
