from flask_security import UserMixin, RoleMixin
from app import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True) 
    roles = db.relationship('Role', secondary='user_roles', backref='users')

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.active,
            "roles": [role.to_dict() for role in self.roles],
        }

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)