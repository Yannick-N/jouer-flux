from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from config import ProdConfig, TestConfig

load_dotenv()

db = SQLAlchemy()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'prod')

    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(ProdConfig)
    
    db.init_app(app)

    from app.routes.firewall_route import firewall_bp
    app.register_blueprint(firewall_bp)

    with app.app_context():
        from .models.firewall import Firewall
        from .models.policy import Policy
        from .models.rule import Rule
        db.create_all()

    return app