import pytest
from unittest import mock
from app import create_app, db

BASE_URL = '/api/v1/firewalls/'

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

@pytest.fixture(autouse=True)
def mock_role_required():
    with mock.patch('app.utils.decorators.role_required', lambda role: lambda f: f):
        yield

def test_create_firewall(client):
    response = client.post(BASE_URL, json={
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
    response = client.post(BASE_URL, json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })    
    firewall_id = response.get_json()['id']
    
    response = client.get(f'{BASE_URL}{firewall_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == firewall_id

def test_update_firewall(client):
    response = client.post(BASE_URL, json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    firewall_id = response.get_json()['id']
    
    response = client.post(f'{BASE_URL}{firewall_id}', json={
        'name': 'Updated Firewall',
        'description': 'Updated description',
        'ip_address': '192.168.1.2'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Firewall'
    assert data['description'] == 'Updated description'
    assert data['ip_address'] == '192.168.1.2'

def test_delete_firewall(client):
    response = client.post(BASE_URL, json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    firewall_id = response.get_json()['id']
    
    response = client.delete(f'{BASE_URL}{firewall_id}')
    assert response.status_code == 204  
    
    response = client.get(f'{BASE_URL}{firewall_id}')
    assert response.status_code == 404  

def test_create_firewall_duplicate_name(client):
    client.post(BASE_URL, json={
        'name': 'Duplicate Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    response = client.post(BASE_URL, json={
        'name': 'Duplicate Firewall',
        'description': 'A second firewall with the same name',
        'ip_address': '192.168.1.2'
    })
    print(response.get_data())
    assert response.status_code == 500 

def test_create_firewall_duplicate_ip(client):
    client.post(BASE_URL, json={
        'name': 'Unique Firewall',
        'description': 'A firewall with a unique IP',
        'ip_address': '192.168.1.3'
    })
    response = client.post(BASE_URL, json={
        'name': 'Another Firewall',
        'description': 'A firewall with a duplicate IP',
        'ip_address': '192.168.1.3'
    })
    assert response.status_code == 500  