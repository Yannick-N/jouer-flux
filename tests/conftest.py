import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app(config_name='test')
    with app.app_context():
        db.create_all()  
        yield app.test_client() 
        db.drop_all() 