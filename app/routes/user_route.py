from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User, Role
from flask_security import SQLAlchemyUserDatastore
from app import db
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema
from app.services.user_service import register_user, login_user, get_user_service, update_user_service, delete_user_service

user_bp = Blueprint("user", __name__)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
user_schema = UserSchema()

@user_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        access_token = login_user(email, password)
        return jsonify(access_token=access_token), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        validated_data = user_schema.load(request.get_json())
        user = register_user(validated_data)
        return jsonify({"msg": "User created successfully", "user": user.to_dict()}), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = get_user_service(id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user = update_user_service(id, data)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        delete_user_service(id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500