def get_rating_text(rating: float) -> str:
    try:
        r = float(rating)
    except Exception:
        r = 0.0

    if r >= 4.5:
        return 'highly rated excellent'
    elif r >= 4.0:
        return 'good quality rated'
    elif r >= 3.5:
        return 'decent quality'
    else:
        return 'affordable'
