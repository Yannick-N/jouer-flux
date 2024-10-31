from app import db
from app.models.firewall import Firewall

def create_firewall(data):
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
