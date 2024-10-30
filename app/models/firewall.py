from .. import db 

class Firewall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    ip_address = db.Column(db.String(15), nullable=False)
    policies = db.relationship('Policy', backref='firewall', lazy=True)

    def __repr__(self):
        return f'<Firewall {self.name}>'