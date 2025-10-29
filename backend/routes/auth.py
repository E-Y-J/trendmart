from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from models.registration import User
from extensions import db
from flask import request, jsonify
from schemas.auth import LoginSchema, TokenResponseSchema, LogoutSchema
# Define blueprint locally to avoid circular imports
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Validate login credentials
        login_data = LoginSchema().load(request.json)

        # Authenticate user (check email/password)
        user = User.query.filter_by(email=login_data['email']).first()
        if not user or not check_password_hash(user.password_hash, login_data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        # Create JWT tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600  # 1 hour
        }

        token_response = TokenResponseSchema().dump(response_data)
        return jsonify(token_response), 200

    except ValidationError as err:
        return jsonify(err.messages), 400


@auth_bp.route('/logout', methods=['POST'])
def logout():

    response_data = {
        "message": "Logged out successfully."
    }

    logout_response = LogoutSchema().dump(response_data)
    return jsonify(logout_response), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():

    try:
        # Get current user ID from the JWT token (convert back to int)
        current_user_id = int(get_jwt_identity())

        # Get user information from database
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get additional token info
        token_claims = get_jwt()

        return jsonify({
            "message": "Hello! You are successfully authenticated!",
            "user_id": current_user_id,
            "email": user.email,
        }), 200

    except Exception as e:
        return jsonify({"error": "Authentication failed"}), 401
