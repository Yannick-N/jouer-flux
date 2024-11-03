import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
from config import ProdConfig, TestConfig

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'prod')

    app = Flask(__name__)

    if config_name == 'test':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(ProdConfig)
    
    db.init_app(app)
    jwt.init_app(app)

    from app.models.user import Role, User
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    from app.routes.firewall_route import firewall_bp
    from app.routes.policy_route import policy_bp    
    from app.routes.rule_route import rule_bp
    from app.routes.user_route import user_bp 

    API_VERSION = "/api/v1"
    app.register_blueprint(firewall_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(policy_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(rule_bp, url_prefix=f"{API_VERSION}/firewalls")
    app.register_blueprint(user_bp, url_prefix=f"{API_VERSION}/user")

    return app