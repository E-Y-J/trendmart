from flask import Blueprint

# Create auth blueprint (for both login and registration)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
swagger_bp = Blueprint('swagger', __name__, url_prefix='/api/docs')
categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')
products_bp = Blueprint('products', __name__, url_prefix='/api/products')

from . import auth
from . import registration
from . import catalog


