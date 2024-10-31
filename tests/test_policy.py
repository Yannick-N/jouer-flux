import pytest
from app import create_app, db

BASE_URL = '/api/policies/'

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

def create_test_firewall(client):
    response = client.post('/api/firewalls/', json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    return response.get_json()['id']

def test_create_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(BASE_URL, json={
        'name': 'Test Policy',
        'firewall_id': firewall_id,
        'status': 'active'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['name'] == 'Test Policy'
    assert data['firewall_id'] == firewall_id
    assert data['status'] == 'active'

def test_get_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(BASE_URL, json={
        'name': 'Test Policy',
        'firewall_id': firewall_id,
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.get(f'{BASE_URL}{policy_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == policy_id
    assert data['firewall_id'] == firewall_id
    assert data['name'] == "Test Policy"

def test_update_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(BASE_URL, json={
        'name': 'Test Policy',
        'firewall_id': firewall_id,
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.post(f'{BASE_URL}{policy_id}', json={
        'name': 'Updated Policy',
        'firewall_id': firewall_id,
        'status': 'inactive'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Policy'
    assert data['status'] == 'inactive'

def test_delete_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(BASE_URL, json={
        'name': 'Test Policy',
        'firewall_id': firewall_id,
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.delete(f'{BASE_URL}{policy_id}')
    assert response.status_code == 204  
    
    response = client.get(f'{BASE_URL}{policy_id}')
    assert response.status_code == 404  