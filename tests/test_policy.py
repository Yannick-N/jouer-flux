import pytest
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

def create_test_firewall(client):
    response = client.post(BASE_URL, json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    return response.get_json()['id']

def test_create_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Test Policy',
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
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Test Policy',
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.get(f'{BASE_URL}{firewall_id}/policies/{policy_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == policy_id
    assert data['firewall_id'] == firewall_id
    assert data['name'] == "Test Policy"

def test_update_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Test Policy',
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}', json={
        'name': 'Updated Policy',
        'status': 'inactive'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Policy'
    assert data['status'] == 'inactive'

def test_delete_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Test Policy',
        'status': 'active'
    })
    policy_id = response.get_json()['id']
    
    response = client.delete(f'{BASE_URL}{firewall_id}/policies/{policy_id}')
    assert response.status_code == 204  
    
    response = client.get(f'{BASE_URL}{firewall_id}/policies/{policy_id}')
    assert response.status_code == 404  

def test_create_policy_with_invalid_firewall(client):
    response = client.post(f'{BASE_URL}999/policies', json={
        'name': 'Invalid Firewall Policy',
        'status': 'active'
    })
    print(f"RESPONSE =>> {response.status_code}")
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == "Firewall with ID 999 does not exist."

def test_create_policy_with_duplicate_name(client):
    firewall_id = create_test_firewall(client)
    
    client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Unique Policy',
        'status': 'active'
    })
    
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Unique Policy',
        'status': 'inactive'
    })
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == "A policy with the name 'Unique Policy' already exists for this firewall."

# def test_update_policy_with_nonexistent_id(client):
#     firewall_id = create_test_firewall(client)
    
#     response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
#         'name': 'Test Policy',
#         'status': 'active'
#     })
#     policy_id = response.get_json()['id'] + 1 
    
#     response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}', json={
#         'name': 'Updated Policy',
#         'status': 'inactive'
#     })
    
#     assert response.status_code == 500
#     data = response.get_json()
#     assert data['error'] == f"Policy with ID {policy_id} does not exist."

def test_delete_nonexistent_policy(client):
    firewall_id = create_test_firewall(client)
    
    response = client.delete(f'{BASE_URL}{firewall_id}/policies/999') 
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Policy with ID 999 does not exist."

def test_get_policies_for_nonexistent_firewall(client):
    response = client.get(f'{BASE_URL}999/policies')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "No policies found for this firewall"