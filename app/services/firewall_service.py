from app import db
from app.models.firewall import Firewall

def create_firewall(data):
    existing_firewall_by_name = db.session.query(Firewall).filter_by(name=data['name']).first()
    if existing_firewall_by_name:
        raise ValueError(f"A firewall with the name '{data['name']}' already exists.")
    
    existing_firewall_by_ip = db.session.query(Firewall).filter_by(ip_address=data['ip_address']).first()
    if existing_firewall_by_ip:
        raise ValueError(f"A firewall with the IP address '{data['ip_address']}' already exists.")
    
    firewall = Firewall(
        name=data['name'],
        description=data['description'],
        ip_address=data['ip_address'],
        policies=data.get('policies', [])
    )
    db.session.add(firewall)
    db.session.commit()
    return firewall

def get_firewall(firewall_id):
    return db.session.get(Firewall, firewall_id)

def update_firewall(firewall_id, data):
    firewall = db.session.get(Firewall, firewall_id)
    if not firewall:
        raise ValueError("Firewall not found")
    
    if 'name' in data:
        existing_firewall = Firewall.query.filter_by(name=data['name']).first()
        if existing_firewall and existing_firewall.id != firewall_id:
            raise ValueError("A firewall with this name already exists.")

    if 'ip_address' in data:
        existing_firewall = Firewall.query.filter_by(ip_address=data['ip_address']).first()
        if existing_firewall and existing_firewall.id != firewall_id:
            raise ValueError("A firewall with this IP address already exists.")

    firewall.name = data.get('name', firewall.name)
    firewall.description = data.get('description', firewall.description)
    firewall.ip_address = data.get('ip_address', firewall.ip_address)
    db.session.commit()
    
    return firewall

def delete_firewall(firewall_id):
    firewall = db.session.get(Firewall, firewall_id)
    if not firewall:
        raise ValueError("Firewall not found")
    
    db.session.delete(firewall)
    db.session.commit()