import pytest
import requests

from halper import Halper
from data import URL, DataRegister, DataLogin, DataUser, DataOrder, random_user_data


@pytest.fixture(scope='function')
def user_data():
    user_data = random_user_data
    return user_data


@pytest.fixture(scope='function')
def create_and_delete_user(user_data):
    response = requests.post(f'{URL}{DataRegister.endpoint}', data=user_data)
    yield response
    headers = {'Authorization': response.json()['accessToken']}
    requests.delete(f'{URL}{DataUser.endpoint}', headers=headers)


@pytest.fixture(scope='function')
def authorize_user(user_data, create_and_delete_user):
    data = {
        'email': user_data['email'],
        'password': user_data['password'],
    }
    response = requests.post(f'{URL}{DataLogin.endpoint}', data=data)
    return response


@pytest.fixture(scope='function')
def create_order(authorize_user):
    headers = {'Authorization': authorize_user.json()['accessToken']}
    data = {"ingredients": ["61c0c5a71d1f82001bdaaa6f"]}
    time = Halper.get_time()
    response = requests.post(f'{URL}{DataOrder.endpoint}', headers=headers, data=data)
    return time, data, response



