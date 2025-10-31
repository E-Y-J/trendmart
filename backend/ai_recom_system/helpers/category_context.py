from typing import List


def get_category_context(name: str, tags: List[str]) -> str:
    name_lower = (name or '').lower()
    tag_text = ' '.join(tags or []).lower()

    # Electronics categories
    if any(word in name_lower for word in ['iphone', 'samsung', 'pixel', 'oneplus']):
        return "smartphone mobile phone cellular device communication"
    if any(word in name_lower for word in ['macbook', 'laptop', 'notebook', 'zenbook']):
        return "laptop computer notebook portable computing"
    if any(word in name_lower for word in ['playstation', 'xbox', 'nintendo', 'console']):
        return "gaming console video game entertainment"

    # Health and Nutrition categories
    if any(word in name_lower for word in ['whey', 'protein', 'creatine', 'supplement']):
        return "nutrition health fitness muscle recovery"
    if any(word in name_lower for word in ['probiotic', 'digestive', 'gut', 'capsule']):
        return "digestive health wellness probiotic supplement"
    if any(word in name_lower for word in ['vitamin', 'multivitamin', 'supplement']):
        return "vitamin nutrition health daily wellness"

    # Food and Snacks categories
    if any(word in tag_text for word in ['chips', 'snack', 'crisps', 'cheese']):
        return "snack food chips crisps savory"
    if any(word in tag_text for word in ['protein-bar', 'bar', 'ready-to-drink']):
        return "protein snack nutrition bar convenient food"

    return "general merchandise product item"
