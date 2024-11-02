from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.firewall_schema import FirewallSchema
from app.services.firewall_service import create_firewall, get_firewalls, get_firewall, update_firewall, delete_firewall

firewall_schema = FirewallSchema()

firewall_bp = Blueprint('firewall', __name__)

@firewall_bp.route('/', methods=['POST'])
def handle_create_firewall():
    try:
        validated_data = firewall_schema.load(request.get_json())
        firewall = create_firewall(validated_data)
        return jsonify(firewall.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/', methods=['GET'])
def handle_get_firewalls():
    try:
        firewalls = get_firewalls()
        return jsonify([firewall.to_dict() for firewall in firewalls]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall_bp.route('/<int:id>', methods=['GET'])
def handle_get_firewall(id):
    try:
        firewall = get_firewall(id)
        if firewall:
            return jsonify(firewall.to_dict()), 200
        return jsonify({"error": "Firewall not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@firewall_bp.route('/<int:id>', methods=['POST'])
def handle_update_firewall(id):
    try:
        firewall_updated = update_firewall(id, request.get_json())
        return jsonify(firewall_updated.to_dict()), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@firewall_bp.route('/<int:id>', methods=['DELETE'])
def handle_delete_firewall(id):
    try:
        delete_firewall(id)
        return '', 204
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500