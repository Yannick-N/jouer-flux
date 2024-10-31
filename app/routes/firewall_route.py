from flask import Blueprint, jsonify, request
from app.services.firewall_service import create_firewall, get_firewall, update_firewall, delete_firewall

firewall_bp = Blueprint('firewall', __name__)

@firewall_bp.route('/', methods=['POST'])
def handle_create_firewall():
    try:
        firewall = create_firewall(request.get_json())
        return jsonify(firewall.to_dict()), 201
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