from unittest import mock
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

@pytest.fixture(autouse=True)
def mock_role_required():
    with mock.patch('app.utils.decorators.role_required', lambda role: lambda f: f):
        yield

def create_test_firewall(client):
    response = client.post(BASE_URL, json={
        'name': 'Test Firewall',
        'description': 'A firewall for testing purposes',
        'ip_address': '192.168.1.1'
    })
    return response.get_json()['id']

def create_test_policy(client, firewall_id):
    response = client.post(f'{BASE_URL}{firewall_id}/policies', json={
        'name': 'Test Policy',
        'status': 'active'
    })
    return response.get_json()['id']

def test_create_rule(client):
    firewall_id = create_test_firewall(client)
    policy_id = create_test_policy(client, firewall_id)

    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules', json={
        'destination_ip': '10.0.0.5',
        'protocol': 'TCP'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['policy_id'] == policy_id
    assert data['destination_ip'] == '10.0.0.5'
    assert data['protocol'] == 'TCP'

def test_get_rule(client):
    firewall_id = create_test_firewall(client)
    policy_id = create_test_policy(client, firewall_id)

    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules', json={
        'destination_ip': '10.0.0.5',
        'protocol': 'UDP'
    })
    rule_id = response.get_json()['id']

    response = client.get(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules/{rule_id}')
    print(f"RESPONSE =>> {response.get_data()}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == rule_id
    assert data['policy_id'] == policy_id
    assert data['destination_ip'] == '10.0.0.5'
    assert data['protocol'] == 'UDP'

def test_update_rule(client):
    firewall_id = create_test_firewall(client)
    policy_id = create_test_policy(client, firewall_id)

    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules', json={
        'destination_ip': '10.0.0.5',
        'protocol': 'TCP'
    })
    rule_id = response.get_json()['id']

    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules/{rule_id}', json={
        'destination_ip': '10.0.0.10',
        'protocol': 'ICMP'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['destination_ip'] == '10.0.0.10'
    assert data['protocol'] == 'ICMP'

def test_delete_rule(client):
    firewall_id = create_test_firewall(client)
    policy_id = create_test_policy(client, firewall_id)

    response = client.post(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules', json={
        'destination_ip': '10.0.0.5',
        'protocol': 'UDP'
    })
    rule_id = response.get_json()['id']

    response = client.delete(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules/{rule_id}')
    assert response.status_code == 204  

    response = client.get(f'{BASE_URL}{firewall_id}/policies/{policy_id}/rules/{rule_id}')
    assert response.status_code == 404