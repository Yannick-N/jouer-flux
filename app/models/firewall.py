from .. import db 

class Firewall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    policies = db.relationship('Policy', backref='firewall', lazy=True, cascade="all")

    def __repr__(self):
        return f'<Firewall {self.name}>'
    
    def to_dict(self):
        firewall_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ip_address": self.ip_address,
            "policies": [policy.to_dict() for policy in self.policies] if self.policies else []
        }
        return firewall_dict