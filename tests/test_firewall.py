import pytest
from app import create_app, db
from app.models.firewall import Firewall

@pytest.fixture
def app():
    app = create_app(config_name='test')  
    with app.app_context():
        db.create_all()  
        yield app
        db.drop_all() 

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_firewall(client):
    response = client.post('/firewalls', json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['name'] == 'Test Firewall'
    assert data['ip_address'] == '192.168.1.1'

def test_get_firewall(client):
    response = client.post('/firewalls', json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes'
    })
    firewall_id = response.get_json()['id']
    
    response = client.get(f'/firewalls/{firewall_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == firewall_id

def test_update_firewall(client):
    response = client.post('/firewalls', json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes'
    })
    firewall_id = response.get_json()['id']
    
    response = client.put(f'/firewalls/{firewall_id}', json={
        'name': 'Updated Firewall',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Firewall'

def test_delete_firewall(client):
    response = client.post('/firewalls', json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes'
    })
    firewall_id = response.get_json()['id']
    
    response = client.delete(f'/firewalls/{firewall_id}')
    assert response.status_code == 204  
    
    response = client.get(f'/firewalls/{firewall_id}')
    assert response.status_code == 404  