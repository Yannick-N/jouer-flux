import os

class Config:
    SECRET_KEY = 'a-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'