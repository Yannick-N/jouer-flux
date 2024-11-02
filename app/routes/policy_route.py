from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.policy_schema import PolicySchema
from app.services.policy_service import create_policy, get_policies_of_firewall, update_policy, delete_policy

policy_schema = PolicySchema()

policy_bp = Blueprint('policy', __name__)

@policy_bp.route('/<int:firewall_id>/policies', methods=['POST'])
def handle_create_policy(firewall_id):
    try:
        validated_data = policy_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id 
        policy = create_policy(validated_data)
        return jsonify(policy.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('<int:firewall_id>/policies', methods=['GET'])
def handle_get_policies(firewall_id):
    try:
        policies = get_policies_of_firewall(firewall_id)
        if policies:
            return jsonify([policy.to_dict() for policy in policies]), 200
        return jsonify({"error": "No policies found for this firewall"}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@policy_bp.route('<int:firewall_id>/policies/<int:policy_id>', methods=['POST'])
def handle_update_policy(firewall_id, policy_id):
    try:
        validated_data = policy_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        validated_data["policy_id"] = policy_id
        updated_policy = update_policy(validated_data)
        return jsonify(updated_policy.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('<int:firewall_id>/policies/<int:policy_id>', methods=['DELETE'])
def handle_delete_policy(firewall_id, policy_id):
    try:
        delete_policy(policy_id)
        return jsonify({"message": f"Policy with ID {policy_id} has been deleted."}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500