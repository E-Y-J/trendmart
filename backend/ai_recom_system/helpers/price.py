def get_price_range(price: float) -> str:
    """Return a short descriptive price-range string for a numeric price."""
    try:
        p = float(price)
    except Exception:
        p = 0.0

    if p < 100:
        return "budget affordable cheap"
    elif p < 500:
        return "mid-range moderate"
    elif p < 1000:
        return "premium quality"
    else:
        return "luxury high-end expensive"
