from sqlalchemy import func
from extensions import db
from models.catalog import Category
from backend.ai_recom_system.helpers.slugify import slugify


def get_or_create_category(name: str):
    '''Retrieve a category by name or slug, or create it if it doesn't exist.
    Returns a tuple of (Category instance, created: bool)
    '''
    if not name:
        raise ValueError('Category name is required')

    slug = slugify(name)
    category = Category.query.filter(
        (Category.slug == slug) | (func.lower(Category.name) == name.lower())).first()
    if not category:
        category = Category(name=name, slug=slug) if hasattr(
            Category, 'slug') else Category(name=name)
        db.session.add(category)
        db.session.flush()  # to get the ID assigned
        return category, True
    return category, False
