import os

class Config:
    SECRET_KEY = 'a-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'