import os

from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from dotenv import load_dotenv
from config import ProdConfig, TestConfig

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'prod')

    app = Flask(__name__)
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Firewall API",
            "description": "API for managing firewalls and users",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    })

    if config_name == 'test':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(ProdConfig)
    
    db.init_app(app)
    jwt.init_app(app)

    from app.models.user import Role, User
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    with app.app_context():
        from .models.firewall import Firewall
        from .models.policy import Policy
        from .models.rule import Rule
        db.create_all() 
        if not user_datastore.find_role("admin"):
            user_datastore.create_role(name="admin", description="Admin Role")
        if not user_datastore.find_role("user"):
            user_datastore.create_role(name="user", description="User Role")
        if not user_datastore.find_user(email="admin@example.com"):
            user_datastore.create_user(
                email="admin@example.com",
                password=generate_password_hash("password", method='pbkdf2:sha256'),
                roles=["admin"],
                fs_uniquifier="admin@example.com"
            )
        db.session.commit()
        print("Database initialized and default user created.")

    from app.routes.firewall_route import firewall_bp
    from app.routes.policy_route import policy_bp    
    from app.routes.rule_route import rule_bp
    from app.routes.user_route import user_bp 

    API_VERSION = "/api/v1"
    app.register_blueprint(firewall_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(policy_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(rule_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(user_bp, url_prefix=f"{API_VERSION}/users")

    return app