from flask import Blueprint, jsonify, request
from app.services.firewall_service import create_firewall

firewall_bp = Blueprint('firewall', __name__)

@firewall_bp.route('/firewalls', methods=['POST'])
def handle_create_firewall():
    try:
        firewall = create_firewall(request.get_json())
        return jsonify(firewall.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500