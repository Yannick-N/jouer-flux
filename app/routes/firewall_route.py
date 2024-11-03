from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.firewall_schema import FirewallSchema
from app.services.firewall_service import create_firewall, get_firewalls, get_firewall, update_firewall, delete_firewall
from app.utils.decorators import role_required

firewall_schema = FirewallSchema()

firewall_bp = Blueprint('firewall', __name__)

@firewall_bp.route('/', methods=['POST'])
@role_required('admin')
def handle_create_firewall():
    """
    Create a new firewall.
    ---
    tags:
      - Firewalls
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            name:
              type: string
              example: "Corporate Firewall"
            description:
              type: string
              example: "Protects corporate network"
            ip_address:
              type: string
              example: "192.168.1.1"
    responses:
      201:
        description: Firewall created successfully.
      400:
        description: Validation error or firewall already exists.
      500:
        description: Internal server error.
    """
    try:
        validated_data = firewall_schema.load(request.get_json())
        firewall = create_firewall(validated_data)
        return jsonify(firewall.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/', methods=['GET'])
def handle_get_firewalls():
    """
    Get all firewalls.
    ---
    tags:
      - Firewalls
    responses:
      200:
        description: A list of firewalls.
      500:
        description: Internal server error.
    """
    try:
        firewalls = get_firewalls()
        return jsonify([firewall.to_dict() for firewall in firewalls]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/<int:id>', methods=['GET'])
def handle_get_firewall(id):
    """
    Get a specific firewall by ID.
    ---
    tags:
      - Firewalls
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Firewall found.
      404:
        description: Firewall not found.
      500:
        description: Internal server error.
    """
    try:
        firewall = get_firewall(id)
        if firewall:
            return jsonify(firewall.to_dict()), 200
        return jsonify({"error": "Firewall not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/<int:id>', methods=['PUT'])
@role_required('admin')
def handle_update_firewall(id):
    """
    Update a firewall by ID.
    ---
    tags:
      - Firewalls
    security:
      - Bearer: []
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
            name:
              type: string
              example: "Updated Firewall"
            description:
              type: string
              example: "Updated description for firewall."
            ip_address:
              type: string
              example: "192.168.1.2"
    responses:
      200:
        description: Firewall updated successfully.
      404:
        description: Firewall not found.
      400:
        description: Validation error.
      500:
        description: Internal server error.
    """
    try:
        firewall_updated = update_firewall(id, request.get_json())
        return jsonify(firewall_updated.to_dict()), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/<int:id>', methods=['DELETE'])
@role_required('admin')
def handle_delete_firewall(id):
    """
    Delete a firewall by ID.
    ---
    tags:
      - Firewalls
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      204:
        description: Firewall deleted successfully.
      404:
        description: Firewall not found.
      500:
        description: Internal server error.
    """
    try:
        delete_firewall(id)
        return '', 204
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500