from flask import Blueprint, jsonify, request
from app.services.policy_service import create_policy, get_policy, update_policy, delete_policy

policy_bp = Blueprint('policy', __name__)

@policy_bp.route('/', methods=['POST'])
def handle_create_policy():
    try:
        policy = create_policy(request.get_json())
        return jsonify(policy.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('/<int:policy_id>', methods=['GET'])
def handle_get_policy(policy_id):
    try:
        policy = get_policy(policy_id)
        if policy:
            return jsonify(policy.to_dict()), 200
        return jsonify({"error": "Policy not found"}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    
@policy_bp.route('/<int:policy_id>', methods=['POST'])
def handle_update_policy(policy_id):
    try:
        updated_policy = update_policy(policy_id, request.get_json())
        return jsonify(updated_policy.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('/<int:policy_id>', methods=['DELETE'])
def handle_delete_policy(policy_id):
    try:
        delete_policy(policy_id)
        return jsonify({"message": f"Policy with ID {policy_id} has been deleted."}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500