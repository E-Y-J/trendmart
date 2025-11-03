from flask import request, jsonify, Blueprint
from schemas.registration import UserRegistrationSchema, CustomerProfileSchema
from extensions import db
from models.registration import User, CustomerProfile

from marshmallow import ValidationError

"""
Customer routes blueprint
- Defined locally to avoid cross-imports with auth.py
"""
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')


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
            phone=validated_data.get('phone'),
        )

        db.session.add(customer_profile)
        db.session.commit()
        return jsonify(CustomerProfileSchema().dump(customer_profile)), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
