from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.policy_schema import PolicySchema
from app.services.policy_service import (
    create_policy, get_policies_of_firewall, get_policy, update_policy, delete_policy
)
from app.utils.decorators import role_required

policy_schema = PolicySchema()
policy_bp = Blueprint('policy', __name__)

@policy_bp.route('/<int:firewall_id>/policies', methods=['POST'])
@role_required('admin')
def handle_create_policy(firewall_id):
    """
    Create a new policy for a firewall.
    ---
    tags:
      - Policies
    security:
      - Bearer: []
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall to associate the policy with.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Allow HTTP Traffic"
            status:
              type: string
              enum: ["active", "inactive"]
              example: "active"
    responses:
      201:
        description: Policy created successfully.
      400:
        description: Validation error.
      500:
        description: Internal server error.
    """
    try:
        validated_data = policy_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        policy = create_policy(validated_data)
        return jsonify(policy.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('<int:firewall_id>/policies', methods=['GET'])
def handle_get_policies(firewall_id):
    """
    Retrieve all policies for a specific firewall.
    ---
    tags:
      - Policies
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall to retrieve policies for.
    responses:
      200:
        description: A list of policies.
        schema:
          type: array
          items:
            $ref: '#/definitions/Policy'
      404:
        description: No policies found for this firewall.
      500:
        description: Internal server error.
    """
    try:
        policies = get_policies_of_firewall(firewall_id)
        if policies:
            return jsonify([policy.to_dict() for policy in policies]), 200
        return jsonify({"error": "No policies found for this firewall"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('<int:firewall_id>/policies/<int:policy_id>', methods=['GET'])
def handle_get_policy(firewall_id, policy_id):
    """
    Retrieve a specific policy by ID for a given firewall.
    ---
    tags:
      - Policies
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the policy.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy to retrieve.
    responses:
      200:
        description: Policy found.
      404:
        description: Policy not found.
      500:
        description: Internal server error.
    """
    try:
        policy = get_policy(firewall_id, policy_id)
        return jsonify(policy.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@policy_bp.route('<int:firewall_id>/policies/<int:policy_id>', methods=['PUT'])
@role_required('admin')
def handle_update_policy(firewall_id, policy_id):
    """
    Update an existing policy for a firewall.
    ---
    tags:
      - Policies
    security:
      - Bearer: []
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the policy.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy to update.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Allow HTTPS Traffic"
            status:
              type: string
              enum: ["active", "inactive"]
              example: "inactive"
    responses:
      200:
        description: Policy updated successfully.
      400:
        description: Validation error.
      404:
        description: Policy not found.
      500:
        description: Internal server error.
    """
    try:
        validated_data = policy_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        validated_data["policy_id"] = policy_id
        updated_policy = update_policy(validated_data)
        return jsonify(updated_policy.to_dict()), 200
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@policy_bp.route('<int:firewall_id>/policies/<int:policy_id>', methods=['DELETE'])
@role_required('admin')
def handle_delete_policy(firewall_id, policy_id):
    """
    Delete a specific policy for a firewall.
    ---
    tags:
      - Policies
    security:
      - Bearer: []
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the policy.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy to delete.
    responses:
      204:
        description: Policy deleted successfully.
      404:
        description: Policy not found.
      500:
        description: Internal server error.
    """
    try:
        delete_policy(policy_id)
        return jsonify({"message": f"Policy with ID {policy_id} has been deleted."}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500