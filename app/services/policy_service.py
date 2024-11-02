from app import db
from app.models.policy import Policy
from app.models.firewall import Firewall

def create_policy(data):
    firewall = db.session.get(Firewall, data['firewall_id'])
    if not firewall:
        raise ValueError(f"Firewall with ID {data['firewall_id']} does not exist.")
    
    status = data.get('status', 'active')
    if status not in ['active', 'inactive']:
        raise ValueError("Invalid status. Must be either 'active' or 'inactive'.")
    
    existing_policy = db.session.query(Policy).filter_by(name=data['name'], firewall_id=data['firewall_id']).first()
    if existing_policy:
        raise ValueError(f"A policy with the name '{data['name']}' already exists for this firewall.")
    
    policy = Policy(
        name=data['name'],
        firewall_id=data['firewall_id'],
        status=status,
    )
    db.session.add(policy)
    db.session.commit()
    return policy

def get_policies_of_firewall(firewall_id):
    return Policy.query.filter_by(firewall_id=firewall_id).all()

def get_policy(firewall_id, policy_id):
    policy = db.session.query(Policy).filter_by(id=policy_id, firewall_id=firewall_id).first()
    if not policy:
        raise ValueError(f"Policy with ID {policy_id} does not exist for this firewall.")
    return policy

def update_policy(data):
    policy = db.session.get(Policy, data["policy_id"])
    new_name = data.get('name', policy.name)
    existing_policy = db.session.query(Policy).filter_by(name=new_name).first()
    
    if existing_policy and existing_policy.id != policy.id:
        raise ValueError(f"A policy with the name '{new_name}' already exists.")

    policy.name = new_name
    policy.status = data.get('status', policy.status)    
    db.session.commit()
    return policy

def delete_policy(policy_id):
    policy = db.session.get(Policy, policy_id)
    if not policy:
        raise ValueError(f"Policy with ID {policy_id} does not exist.")
    
    db.session.delete(policy)
    db.session.commit()