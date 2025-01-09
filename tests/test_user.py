import allure
import pytest
import requests
from data import DataUser, URL


class TestUser:

    @allure.title('Изменение данных пользователя - авторизованный пользователь - успешное изменение')
    @pytest.mark.parametrize('data, result', DataUser.dataset_successful_change_fields)
    def test_user_change_data_with_token_successful(self, authorize_user, data, result):
        headers = {'Authorization': authorize_user.json()['accessToken']}
        response = requests.patch(f'{URL}{DataUser.endpoint}', headers=headers, data=data)
        response_json = response.json()

        assert (response.status_code == 200 and
                response_json['success'] == True and
                response_json['user'] == result)

    @allure.title('Изменение данных пользователя - неавторизованный пользователь - изменение запрещено')
    @pytest.mark.parametrize('data, result', DataUser.dataset_failed_change_fields)
    def test_user_change_data_without_token_failed_change(self, authorize_user, data, result):

        response_path = requests.patch(f'{URL}{DataUser.endpoint}', data=data)
        response_path_json = response_path.json()

        headers = {'Authorization': authorize_user.json()['accessToken']}
        response_get = requests.get(f'{URL}{DataUser.endpoint}', headers=headers)
        response_get_json = response_get.json()

        assert (response_path.status_code == 401 and
                response_path_json == DataUser.error_change_user_data and
                response_get_json['user'] == result)
