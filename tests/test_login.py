import re
import pytest
import requests
import allure
from data import DataLogin, URL


class TestLogin:
    @allure.title('Авторизация пользователя - успешная авторизация')
    def test_login_successful_authorization(self, user_data, authorize_user):
        response = authorize_user.json()

        assert (authorize_user.status_code == 200 and
                response['success'] == True and
                response['user']['email'] == user_data['email'] and
                response['user']['name'] == user_data['name'] and
                re.match(r"^Bearer .+$", response['accessToken']) and
                re.match(r"^.+$", response['refreshToken']))

    @allure.title('Авторизация пользователя - без обязательный полей - ошибка "email or password are incorrect"')
    @pytest.mark.parametrize('data', DataLogin.dataset_fields)
    def test_login_without_require_fields_error_authorization(self, create_and_delete_user, data):
        response = requests.post(f'{URL}{DataLogin.endpoint}', data=data)

        assert (response.status_code == 401 and
                response.json() == DataLogin.error_incorrect_data)
