from .. import db

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firewall_id = db.Column(db.Integer, db.ForeignKey('firewall.id'), nullable=False)
    rules = db.relationship('Rule', backref='policy', lazy=True)