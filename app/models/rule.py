from .. import db
import datetime

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    destination_ip = db.Column(db.String(45), nullable=True)
    protocol = db.Column(db.String(20), nullable=True)  # 'TCP', 'UDP', 'ICMP'
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }