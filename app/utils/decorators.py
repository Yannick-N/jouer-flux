from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            
            user_id = get_jwt_identity()
            
            user = User.query.get(user_id)
            if user is None or required_role not in [role.name for role in user.roles]:
                return jsonify({"msg": "Unauthorized"}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator