from flask import request, current_app
from typing import List, Dict, Any, Optional
from sqlalchemy import func
from extensions import db
from models.catalog import Product
from models.shopping import OrderItem
from .recommendation import recom_bp, _req_id, _now_ms, _json_response


def product_model_to_card(product: Product, score: Optional[float] = None) -> Dict[str, Any]:
    """Convert a Product ORM model into a product card dictionary.

    Falls back gracefully when optional fields or relationships are missing.
    """
    subcategory = getattr(product, "subcategory", None)
    category = getattr(subcategory, "category", None) if subcategory else None
    # Normalize tags from CSV into list
    raw_tags = getattr(product, "tags", None)
    if isinstance(raw_tags, str):
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    elif isinstance(raw_tags, (list, tuple)):
        tags = [str(t).strip() for t in raw_tags if t]
    else:
        tags = []

    primary_image = getattr(product, "image_url", None)
    images = [primary_image] if primary_image else []

    card = {
        "id": getattr(product, "id", None),
        "sku": getattr(product, "sku", None),
        "name": getattr(product, "name", "") or "",
        "description": getattr(product, "description", "") or "",
        "price": float(getattr(product, "price", 0.0) or 0.0),
        "rating": float(getattr(product, "rating", 0.0) or 0.0),  # optional
        "tags": tags,
        "primary_image": primary_image,
        "thumbnail": getattr(product, "image_thumb_url", None),
        "images": images,
        "subcategory": getattr(subcategory, "name", None) if subcategory else None,
        "main_category": getattr(category, "name", None) if category else None,
        "category_info": None,
        "times_click_on": int(getattr(product, "times_click_on", 0) or 0),
    }
    if score is not None:
        card["score"] = float(score)
    return card


def _get_top_sold_products(limit: int = 10) -> List[Product]:
    """Return products ordered by units sold (descending), then most viewed, then id.

    Uses a subquery for aggregate sales to avoid GROUP BY issues on full Product rows.
    """
    sales_subquery = (
        db.session.query(
            OrderItem.product_id.label("product_id"),
            func.sum(OrderItem.quantity).label("units_sold"),
        )
        .group_by(OrderItem.product_id)
        .subquery()
    )

    units_sold_expr = func.coalesce(sales_subquery.c.units_sold, 0)

    query = (
        db.session.query(Product)
        .outerjoin(sales_subquery, sales_subquery.c.product_id == Product.id)
        .order_by(units_sold_expr.desc(), Product.times_click_on.desc(), Product.id.asc())
        .limit(limit)
    )
    return list(query.all())


def _get_top_viewed_products(limit: int = 10) -> List[Product]:
    """Fallback: return products ordered by most viewed, then id."""
    query = (
        db.session.query(Product)
        .order_by(Product.times_click_on.desc(), Product.id.asc())
        .limit(limit)
    )
    return list(query.all())


@recom_bp.route('/cold_start', methods=['GET'])
def cold_start_feed():
    """Cold-start recommendation feed for new users.

    Returns top sold products (by total quantity across orders). If there are
    no sales yet, falls back to most viewed (times_click_on) then by id.

    Query parameters:
      - top_k: number of products to return (default 10)
    """
    request_id = _req_id()
    start_ms = _now_ms()
    top_k = request.args.get('top_k', 10, type=int)
    try:
        products = _get_top_sold_products(limit=top_k)
        if not products:
            products = _get_top_viewed_products(limit=top_k)
        items = [product_model_to_card(p) for p in products]
        elapsed_ms = _now_ms() - start_ms
        current_app.logger.info(
            f"[recommendations.cold_start] request_id={request_id} top_k={top_k} result_count={len(items)} elapsed_ms={elapsed_ms}")
        return _json_response({"results": items, "count": len(items), "elapsed_ms": elapsed_ms}, req_id=request_id)
    except Exception as exc:
        current_app.logger.exception(
            f"[recommendations.cold_start] request_id={request_id} failed: {exc}")
        return _json_response({"error": str(exc)}, 500, request_id)
