from flask import Blueprint, jsonify, request
from app.services.rule_service import create_rule, get_rule, update_rule, delete_rule

rule_bp = Blueprint('rules', __name__)

@rule_bp.route('/', methods=['POST'])
def handle_create_rule():
    rule = create_rule(request.get_json())
    return jsonify(rule.to_dict()), 201

@rule_bp.route('/<int:rule_id>', methods=['GET'])
def handle_get_rule(rule_id):
    rule = get_rule(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found"}), 404
    return jsonify(rule.to_dict()), 200

@rule_bp.route('/<int:rule_id>', methods=['PUT'])
def handle_update_rule(rule_id):
    data = request.get_json()
    try:
        rule = update_rule(rule_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify(rule.to_dict()), 200

@rule_bp.route('/<int:rule_id>', methods=['DELETE'])
def handle_delete_rule(rule_id):
    try:
        delete_rule(rule_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return '', 204