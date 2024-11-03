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
    """
    Login user and retrieve an access token.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            email:
              type: string
              example: "admin@example.com"
            password:
              type: string
              example: "password"
    responses:
      200:
        description: Login successful, access token returned.
        schema:
          properties:
            access_token:
              type: string
              example: "eyJ0eXAiOiJKV1QiLCJh..."
      401:
        description: Unauthorized - Invalid credentials.
    """
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        access_token = login_user(email, password)
        return jsonify(access_token=access_token), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            email:
              type: string
              example: "newuser@example.com"
            password:
              type: string
              example: "strongpassword"
    responses:
      201:
        description: User created successfully.
      400:
        description: Validation error or user already exists.
      500:
        description: Internal server error.
    """
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
    """
    Get a user by ID.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: User found.
      404:
        description: User not found.
      500:
        description: Internal server error.
    """
    try:
        user = get_user_service(id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Update a user by ID.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          properties:
            email:
              type: string
              example: "updateduser@example.com"
            password:
              type: string
              example: "newpassword"
    responses:
      200:
        description: User updated successfully.
      404:
        description: User not found.
      500:
        description: Internal server error.
    """
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
    """
    Delete a user by ID.
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      204:
        description: User deleted successfully.
      404:
        description: User not found.
      500:
        description: Internal server error.
    """
    try:
        delete_user_service(id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500