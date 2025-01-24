import requests
from http import HTTPStatus


def test_status(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK, 'Service unavailable'


def test_data_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK, f'Expected status code 200, but got {response.status_code}'
    assert bool(response.json()['items']) is True, 'Data did not load'