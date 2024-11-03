from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.rule_schema import RuleSchema
from app.services.rule_service import create_rule, get_rules_of_policy, get_rule, update_rule, delete_rule
from app.utils.decorators import role_required

rule_schema = RuleSchema()

rule_bp = Blueprint('rule', __name__)

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules', methods=['POST'])
@role_required('admin')
def handle_create_rule(firewall_id, policy_id):
    """
    Create a new rule for a policy under a specific firewall.
    ---
    tags:
      - Rules
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
        description: ID of the policy to associate the rule with.
      - in: body
        name: body
        required: true
        schema:
          properties:
            protocol:
              type: string
              example: "tcp"
            destination_ip:
              type: string
              example: "10.0.0.20"
    responses:
      201:
        description: Rule created successfully.
      400:
        description: Validation error.
      500:
        description: Internal server error.
    """
    try:
        validated_data = rule_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        validated_data["policy_id"] = policy_id
        rule = create_rule(validated_data)
        return jsonify(rule.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules', methods=['GET'])
def handle_get_rules(firewall_id, policy_id):
    """
    Retrieve all rules for a specific policy under a given firewall.
    ---
    tags:
      - Rules
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
        description: ID of the policy to retrieve rules for.
    responses:
      200:
        description: A list of rules.
        schema:
          type: array
          items:
            $ref: '#/definitions/Rule'
      404:
        description: No rules found for this policy.
      500:
        description: Internal server error.
    """
    try:
        rules = get_rules_of_policy(policy_id)
        if not rules:
            return jsonify({"error": "No rules found for this policy"}), 404
        return jsonify([rule.to_dict() for rule in rules]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules/<int:rule_id>', methods=['GET'])
def get_rule_route(firewall_id, policy_id, rule_id):
    """
    Retrieve a specific rule by ID for a given policy and firewall.
    ---
    tags:
      - Rules
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the rule.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy associated with the rule.
      - in: path
        name: rule_id
        required: true
        type: integer
        description: ID of the rule to retrieve.
    responses:
      200:
        description: Rule found.
      404:
        description: Rule not found.
      500:
        description: Internal server error.
    """
    try:
        rule = get_rule(rule_id)
        return jsonify(rule.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules/<int:rule_id>', methods=['PUT'])
@role_required('admin')
def handle_update_rule(firewall_id, policy_id, rule_id):
    """
    Update an existing rule for a policy under a specific firewall.
    ---
    tags:
      - Rules
    security:
      - Bearer: []
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the rule.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy associated with the rule.
      - in: path
        name: rule_id
        required: true
        type: integer
        description: ID of the rule to update.
      - in: body
        name: body
        required: true
        schema:
          properties:
            protocol:
              type: string
              example: "udp"
            destination_ip:
              type: string
              example: "10.0.0.25"
    responses:
      200:
        description: Rule updated successfully.
      400:
        description: Validation error.
      404:
        description: Rule not found.
      500:
        description: Internal server error.
    """
    try:
        validated_data = rule_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        validated_data["policy_id"] = policy_id
        validated_data["rule_id"] = rule_id
        rule = update_rule(validated_data)
        return jsonify(rule.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules/<int:rule_id>', methods=['DELETE'])
@role_required('admin')
def handle_delete_rule(firewall_id, policy_id, rule_id):
    """
    Delete a specific rule for a policy under a specific firewall.
    ---
    tags:
      - Rules
    security:
      - Bearer: []
    parameters:
      - in: path
        name: firewall_id
        required: true
        type: integer
        description: ID of the firewall associated with the rule.
      - in: path
        name: policy_id
        required: true
        type: integer
        description: ID of the policy associated with the rule.
      - in: path
        name: rule_id
        required: true
        type: integer
        description: ID of the rule to delete.
    responses:
      204:
        description: Rule deleted successfully.
      404:
        description: Rule not found.
      500:
        description: Internal server error.
    """
    try:
        delete_rule(rule_id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500