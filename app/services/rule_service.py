from app.models.firewall import Firewall
from app.models.policy import Policy
from app.models.rule import Rule
from app import db


def create_rule(data):
    firewall = db.session.get(Firewall, data['firewall_id'])
    if not firewall:
        raise ValueError(f"Firewall with ID {policy.firewall_id} does not exist for the given policy.")
    
    policy = db.session.get(Policy, data['policy_id'])
    if not policy:
        raise ValueError(f"Policy with ID {data['policy_id']} does not exist.")

    
    if not data.get('destination_ip') or not data.get('protocol'):
        raise ValueError("Destination IP and protocol are required.")

    rule = Rule(
        policy_id=data['policy_id'],
        destination_ip=data.get('destination_ip'),
        protocol=data.get('protocol')
    )
    db.session.add(rule)
    db.session.commit()
    return rule

def get_rules_of_policy(policy_id):
    return Rule.query.filter_by(policy_id=policy_id).all()

def get_rule(rule_id):
    rule = db.session.get(Rule, rule_id)
    if not rule:
        raise ValueError(f"Rule with ID {rule_id} does not exist.")
    return rule

def update_rule(data):
    rule = db.session.get(Rule, data['rule_id'])
    if not rule:
        raise ValueError(f"Rule with ID {data['rule_id']} does not exist.")

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