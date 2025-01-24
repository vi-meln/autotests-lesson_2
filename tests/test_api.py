import pytest
import requests
import json
from http import HTTPStatus
from src.models.User import User


@pytest.fixture()
def len_data():
    with open("mocks/users.json") as f:
        users = json.load(f)
    return len(users)


# Default: size (default=50, min=1, max=100), page (default=1, min=1)

def test_users_without_parameters(app_url, len_data):
    """Отправка запроса без параметров. ОР: Получение значений по умолчанию"""

    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK, f'Expected status code 200, but got {response.status_code}'
    response_body = response.json()
    assert response_body['total'] == len(response_body['items']) == len_data, 'Incorrect total quantity'
    assert response_body['page'] == 1, 'Incorrect page number'
    assert response_body['size'] == 50, 'Incorrect size'

    users = response.json()['items']
    for user in users:
        User.model_validate(user)


@pytest.mark.parametrize("page, size", [(1, 2),
                                        (2, 5),
                                        (3, 4)])
def test_users_with_parameters(app_url, page, size):
    """Отправка запроса с параметрами page и size"""
    response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": size})
    assert response.status_code == HTTPStatus.OK, f'Expected status code 200, but got {response.status_code}'
    response_body = response.json()
    assert len(response_body['items']) == size, 'Incorrect amount of data'
    assert response_body['page'] == page, 'Incorrect page number'
    assert response_body['size'] == size, 'Incorrect size'

    users = response.json()['items']
    for user in users:
        User.model_validate(user)


def test_users_correct_user(app_url):
    """Проверяем что на последующей странице user_id первого объекта больше,
    чем user_id у последнего объекта на предыдущей странице"""
    response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": 3})
    assert response.status_code == HTTPStatus.OK, f'Expected status code 200, but got {response.status_code}'
    response_body = response.json()
    last_item_page_1 = response_body['items'][-1]

    response = requests.get(f"{app_url}/api/users/", params={"page": 2, "size": 3})
    assert response.status_code == HTTPStatus.OK, f'Expected status code 200, but got {response.status_code}'
    response_body = response.json()
    first_item_page_2 = response_body['items'][0]
    assert first_item_page_2["id"] > last_item_page_1["id"]


@pytest.mark.parametrize("page", [-1, 0, "rty"])
def test_users_invalid_page(app_url, page):
    """Проверяем невалидные значения для параметра page"""
    response = requests.get(f"{app_url}/api/users/", params={"page": page})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("size", [-1, 0, "rty", 101])
def test_users_invalid_size(app_url, size):
    """Проверяем невалидные значения для параметра size (прим: по умолчанию max_size=100)"""
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_users_no_data_items(app_url, len_data):
    response = requests.get(f"{app_url}/api/users/", params={"page": 10})
    assert response.status_code == HTTPStatus.OK
    response_body = response.json()
    assert bool(response_body['items']) is False
    assert response_body['total'] == len_data, 'Incorrect amount of data'
    assert response_body['page'] == 10, 'Incorrect page number'
    assert response_body['size'] == 50, 'Incorrect size'
