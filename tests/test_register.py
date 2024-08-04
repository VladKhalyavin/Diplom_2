import re
import allure
import pytest
import requests
from data import URL, DataRegister


class TestRegistration:

    @allure.title('Регистарция пользователя - новый пользователь - успешная регистрация')
    def test_register_successful_registration(self, user_data, create_and_delete_user):
        response = create_and_delete_user.json()

        assert (create_and_delete_user.status_code == 200 and
                response['success'] == True and
                response['user']['email'] == user_data['email'] and
                response['user']['name'] == user_data['name'] and
                re.match(r"^Bearer .+$", response['accessToken']) and
                re.match(r"^.+$", response['refreshToken']))

    @allure.title('Регистарция пользователя - уже существующий пользователь - ошибка "User already exists"')
    def test_register_existing_user_user_already_exists(self, user_data, create_and_delete_user):
        response = requests.post(f'{URL}{DataRegister.endpoint}', data=user_data)

        assert (response.status_code == 403 and
                response.json() == DataRegister.error_existing_user)

    @allure.title('Регистарция пользователя - без обязательных полей - ошибка "Email, password and name are required '
                  'fields"')
    @pytest.mark.parametrize('data', DataRegister.dataset_fields)
    def test_register_existing_user_user_already_exists(self, data):
        response = requests.post(f'{URL}{DataRegister.endpoint}', data=data)

        assert (response.status_code == 403 and
                response.json() == DataRegister.error_fields_missing)
