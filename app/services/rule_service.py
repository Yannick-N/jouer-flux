from marshmallow import ValidationError
from app.models.policy import Policy
from app.models.rule import Rule
from app import db
from app.schemas.rule_schema import RuleSchema

rule_schema = RuleSchema()

def create_rule(data):
    try:
        validated_data = rule_schema.load(data)
    except ValidationError as err:
        raise ValueError({"error": err.messages})

    policy = db.session.get(Policy, data['policy_id'])
    if not policy:
        raise ValueError(f"Policy with ID {data['policy_id']} does not exist.")

    rule = Rule(
        policy_id=validated_data['policy_id'],
        destination_ip=validated_data.get('destination_ip'),
        protocol=validated_data.get('protocol')
    )
    db.session.add(rule)
    db.session.commit()
    return rule

def get_rule(rule_id):
    return db.session.get(Rule, rule_id)

def update_rule(rule_id, data):
    rule = db.session.get(Rule, rule_id)
    if not rule:
        raise ValueError(f"Rule with ID {rule_id} does not exist.")

    rule.destination_ip = data.get('destination_ip', rule.destination_ip)
    rule.protocol = data.get('protocol', rule.protocol)
    db.session.commit()
    return rule

def delete_rule(rule_id):
    rule = db.session.get(Rule, rule_id)
    if not rule:
        raise ValueError(f"Rule with ID {rule_id} does not exist.")
    
    db.session.delete(rule)
    db.session.commit()