from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from schemas.registration import UserSchema, UserRegistrationSchema, CustomerProfileSchema, AddressSchema
from extensions import db
from models.registration import User, CustomerProfile, Address
from werkzeug.security import generate_password_hash
from sqlalchemy import select, delete
from marshmallow import ValidationError


# Create the admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/register', methods=['POST'])
def register_admin_user():
    try:
        user_data = request.json

        # Validate the input data using schema
        validated_data = UserRegistrationSchema().load(user_data)

        # Check if email already exists
        email_exist = db.session.execute(
            select(User).filter_by(email=validated_data['email'])
        ).scalar_one_or_none()

        if email_exist:
            return jsonify({"status": "error", "message": "A user with this email already exists!"}), 400

        # Hash the password
        password = validated_data.get('password')
        if not password:
            return jsonify({"error": "Password is required"}), 400

        # Create User instance
        user = User(
            email=validated_data['email'],
            password_hash=generate_password_hash(password),
            role='admin'
        )

        db.session.add(user)
        db.session.commit()

        # Auto-login after registration
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "user": UserSchema().dump(user),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    
@admin_bp.route('/manage_users', methods=['GET'])
@jwt_required()
def manage_users():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User, current_user_id)
    
    # Check if user exists
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    # if user role is not admin
    if current_user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    
    # Get all users
    users = db.session.execute(select(User)).scalars().all()
    return jsonify({"message": "Users retrieved successfully", "users": UserSchema(many=True).dump(users)}), 200

@admin_bp.route('/manage_users/<int:user_id>', methods=['GET'])
@jwt_required()
def manage_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User, current_user_id)
    
    # Check if user exists
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    # if user role is not admin
    if current_user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403

    # Get user by ID
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User retrieved successfully", "user": UserSchema().dump(user)}), 200

@admin_bp.route('/manage_users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User, current_user_id)
    
    # Check if user exists
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    # if user role is not admin
    if current_user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403

    # Get user by ID
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update user fields
    for key, value in request.json.items():
        if key != "id": # Prevent updating the ID
            setattr(user, key, value)

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": UserSchema().dump(user)}), 200

@admin_bp.route('/manage_users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User, current_user_id)
    
    # Check if user exists
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    # if user role is not admin
    if current_user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403

    #prevent delete of self
    if current_user.id == user_id:
        return jsonify({"message": "Access forbidden: Cannot delete self"}), 403

    # Get user by ID
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200