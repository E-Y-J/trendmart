from flask import request, jsonify
from schemas.registration import UserRegistrationSchema, CustomerProfileSchema
# Import blueprints from auth module to avoid circular imports
from .auth import auth_bp, customer_bp
from extensions import db
from models.registration import User, CustomerProfile
from werkzeug.security import generate_password_hash
from sqlalchemy import select, delete
from marshmallow import ValidationError


@auth_bp.route('/register', methods=['POST'])
def register():
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
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()
        return jsonify(UserRegistrationSchema().dump(user)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400


@customer_bp.route('/profile', methods=['POST'])
def create_customer_profile():
    try:
        profile_data = request.json

        # Validate the input data using schema
        validated_data = CustomerProfileSchema().load(profile_data)

        user_id = validated_data.get('user_id')
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create CustomerProfile instance
        customer_profile = CustomerProfile(
            user_id=user_id,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone')
        )

        db.session.add(customer_profile)
        db.session.commit()
        return jsonify(CustomerProfileSchema().dump(customer_profile)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
