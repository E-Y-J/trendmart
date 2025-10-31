
def product_to_dict(product):
    raw_tags = getattr(product, 'tags', None)
    if isinstance(raw_tags, str):
        tags = [t.strip() for t in raw_tags.split(',') if t.strip()]
    elif isinstance(raw_tags, (list, tuple)):
        tags = [str(t).strip() for t in raw_tags if t]
    else:
        tags = []

    subcategory = getattr(product, 'subcategory', None)
    category = getattr(subcategory, 'category',
                       None) if subcategory is not None else None

    return {
        "id": int(getattr(product, "id", None)) if getattr(product, "id", None) is not None else None,
        "sku": getattr(product, "sku", None),
        "name": (getattr(product, "name", "") or ""),
        "description": (getattr(product, "description", "") or ""),
        "price": float(getattr(product, "price", 0.0) or 0.0),
        "rating": float(getattr(product, "rating", 0.0) or 0.0),
        "tags": tags,
        "primary_image": getattr(product, "product_img", None),
        "images": getattr(product, "images", []) or [],
        "subcategory": getattr(subcategory, "name", None) if subcategory else None,
        "main_category": getattr(category, "name", None) if category else None,
        "times_click_on": int(getattr(product, "times_click_on", 0) or 0),
    }
