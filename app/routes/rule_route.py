from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.rule_schema import RuleSchema
from app.services.rule_service import create_rule, get_rules_of_policy, get_rule, update_rule, delete_rule

rule_schema = RuleSchema()

rule_bp = Blueprint('rule', __name__)

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules', methods=['POST'])
def handle_create_rule(firewall_id, policy_id):
    try:
        validated_data = rule_schema.load(request.get_json())
        validated_data["firewall_id"] = firewall_id
        validated_data["policy_id"] = policy_id
        rule = create_rule(validated_data)
        return jsonify(rule.to_dict()), 201
    except ValidationError as err:
        return jsonify({"error": err.messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules', methods=['GET'])
def handle_get_rule(firewall_id, policy_id):
    try:
        rules = get_rules_of_policy(policy_id)
        if not rules:
            return jsonify({"error": "Rule not found"}), 404
        return jsonify([rule.to_dict() for rule in rules]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules/<int:rule_id>', methods=['GET'])
def get_rule_route(firewall_id, policy_id, rule_id):
    try:
        rule = get_rule(rule_id)
        return jsonify(rule.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 

@rule_bp.route('/<int:firewall_id>/policies/<int:policy_id>/rules/<int:rule_id>', methods=['POST'])
def handle_update_rule(firewall_id, policy_id, rule_id):
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
def handle_delete_rule(firewall_id, policy_id, rule_id):
    try:
        delete_rule(rule_id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500