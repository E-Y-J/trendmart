from flask import Blueprint

# Create auth blueprint (for both login and registration)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
swagger_bp = Blueprint('swagger', __name__, url_prefix='/api/docs')
customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')

from . import auth
from . import registration


