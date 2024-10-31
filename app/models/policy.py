from .. import db
import datetime


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    firewall_id = db.Column(db.Integer, db.ForeignKey('firewall.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    status = db.Column(db.String(20), default='active')
    rules = db.relationship('Rule', backref='policy', lazy=True)

    def __repr__(self):
        return f'<Policy {self.name}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "firewall_id": self.firewall_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "status": self.status,
            "rules": [rule.to_dict() for rule in self.rules] if self.rules else []
        }