from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity, jwt_required
from extensions import db
from models.recommendation_feedback import ProductInteraction, RecommendationFeedback
from models.catalog import Product
from schemas.feedback import ProductInteractionCreateSchema, RecommendationFeedbackCreateSchema
from sqlalchemy.exc import IntegrityError
import json

events_bp = Blueprint("events", __name__, url_prefix="/events")
# Use a distinct blueprint name and align prefix with existing recommendations namespace
recom_feedback_bp = Blueprint(
    "recommendation_feedback", __name__, url_prefix="/recommendations"
)


@events_bp.route("/view", methods=["POST"])
def record_view():
    if not request.is_json:
        return jsonify({"error": "bad_request", "message": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "message": "Request body must be valid JSON"}), 400
    try:
        data = ProductInteractionCreateSchema().load(
            {**payload, "event_type": "view"})
    except ValidationError as err:
        return jsonify({"error": "validation_error", "messages": err.messages}), 400
    # Validate product existence early to avoid FK IntegrityError
    if not Product.query.get(data["product_id"]):
        return jsonify({"error": "not_found", "message": "product does not exist"}), 404
    # If source missing but provided under context_json, promote it
    if not data.get("source") and isinstance(payload.get("context_json"), dict):
        data["source"] = payload["context_json"].get("source")
    if isinstance(data.get("context_json"), dict):
        data["context_json"] = json.dumps(data["context_json"])
    if "user_id" not in data:
        # try JWT if available
        try:
            data["user_id"] = int(get_jwt_identity())
        except Exception:
            pass
    interaction = ProductInteraction(**data)
    db.session.add(interaction)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "db_integrity_error", "message": str(e.orig)}), 400
    return jsonify({"status": "ok"}), 201


@events_bp.route("/cart_add", methods=["POST"])
def record_cart_add():
    if not request.is_json:
        return jsonify({"error": "bad_request", "message": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "message": "Request body must be valid JSON"}), 400
    try:
        data = ProductInteractionCreateSchema().load(
            {**payload, "event_type": "add_to_cart"})
    except ValidationError as err:
        return jsonify({"error": "validation_error", "messages": err.messages}), 400
    if not Product.query.get(data["product_id"]):
        return jsonify({"error": "not_found", "message": "product does not exist"}), 404
    if not data.get("source") and isinstance(payload.get("context_json"), dict):
        data["source"] = payload["context_json"].get("source")
    if isinstance(data.get("context_json"), dict):
        data["context_json"] = json.dumps(data["context_json"])
    if "user_id" not in data:
        try:
            data["user_id"] = int(get_jwt_identity())
        except Exception:
            pass
    interaction = ProductInteraction(**data)
    db.session.add(interaction)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "db_integrity_error", "message": str(e.orig)}), 400
    return jsonify({"status": "ok"}), 201


@events_bp.route("/purchase", methods=["POST"])
def record_purchase():
    if not request.is_json:
        return jsonify({"error": "bad_request", "message": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "message": "Request body must be valid JSON"}), 400
    try:
        data = ProductInteractionCreateSchema().load(
            {**payload, "event_type": "purchase"})
    except ValidationError as err:
        return jsonify({"error": "validation_error", "messages": err.messages}), 400
    if not Product.query.get(data["product_id"]):
        return jsonify({"error": "not_found", "message": "product does not exist"}), 404
    if not data.get("source") and isinstance(payload.get("context_json"), dict):
        data["source"] = payload["context_json"].get("source")
    if isinstance(data.get("context_json"), dict):
        data["context_json"] = json.dumps(data["context_json"])
    if "user_id" not in data:
        try:
            data["user_id"] = int(get_jwt_identity())
        except Exception:
            pass
    interaction = ProductInteraction(**data)
    db.session.add(interaction)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "db_integrity_error", "message": str(e.orig)}), 400
    return jsonify({"status": "ok"}), 201


@recom_feedback_bp.route("/feedback", methods=["POST"])
def recommendation_feedback():
    if not request.is_json:
        return jsonify({"error": "bad_request", "message": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "message": "Request body must be valid JSON"}), 400
    try:
        data = RecommendationFeedbackCreateSchema().load(payload)
    except ValidationError as err:
        return jsonify({"error": "validation_error", "messages": err.messages}), 400
    # Validate product exists to avoid FK failures
    if not Product.query.get(data["product_id"]):
        return jsonify({"error": "not_found", "message": "product does not exist"}), 404
    # fallback user id
    if data.get("user_id") is None:
        try:
            from flask_jwt_extended import get_jwt_identity
            data["user_id"] = int(get_jwt_identity())
        except Exception:
            pass
    fb = RecommendationFeedback(**data)
    db.session.add(fb)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "db_integrity_error", "message": str(e.orig)}), 400
    return jsonify({"status": "ok"}), 201
