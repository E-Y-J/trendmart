from sqlalchemy import func
from extensions import db
from models.catalog import Subcategory
from backend.ai_recom_system.helpers.slugify import slugify


def get_or_create_subcategory(name: str, category_id: int):
    if not name:
        raise ValueError('Subcategory name is required')
    if not category_id:
        raise ValueError('Category ID is required')

    slug = slugify(name)
    subcategory = Subcategory.query.filter((Subcategory.slug == slug) | ((func.lower(Subcategory.name) == name.lower()) & (Subcategory.category_id == category_id))
                                           ).first()

    if not subcategory:
        subcategory = Subcategory(
            name=name, slug=slug, category_id=category_id)
        db.session.add(subcategory)
        db.session.flush()  # assign ID without committing
        return subcategory, True

    return subcategory, False
