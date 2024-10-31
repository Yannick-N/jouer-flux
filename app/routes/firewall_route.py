from flask import Blueprint, jsonify, request
from app.services.firewall_service import create_firewall, get_firewall

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