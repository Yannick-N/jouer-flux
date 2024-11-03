from werkzeug.security import check_password_hash, generate_password_hash
from flask_security import SQLAlchemyUserDatastore
from app import db
from app.models.user import User, Role
from flask_jwt_extended import create_access_token

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return create_access_token(identity=user.id)
    raise ValueError("Bad credentials")

def register_user(data):
    if user_datastore.find_user(email=data['email']):
        raise ValueError("User already exists")
    
    user = user_datastore.create_user(
        email=data['email'],
        password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        roles=["user"],
        fs_uniquifier=data['email']
    )
    
    db.session.commit()
    return user

def get_user_service(user_id):
    return User.query.get(user_id)

def update_user_service(user_id, data):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already in use")

    if 'password' in data:
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return user

def delete_user_service(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    db.session.delete(user)
    db.session.commit()