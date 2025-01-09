import re
import allure
import pytest
import requests
from data import DataOrder, URL
from halper import Halper


class TestOrder:

    @allure.title('Создание заказа - авторизованны пользователь - успешное создание заказа')
    @pytest.mark.parametrize('data', DataOrder.dataset_ingredients)
    def test_order_with_authorization_successful_order(self, user_data, authorize_user, data):
        headers = {'Authorization': authorize_user.json()['accessToken']}
        time = Halper.get_time()
        response = requests.post(f'{URL}{DataOrder.endpoint}', headers=headers, data=data['body'])
        r_json = response.json()

        assert (response.status_code == 200 and
                r_json['success'] == True and
                r_json['name'] == data['name'] and
                r_json['order']['ingredients'] == Halper.collect_order(data['body']['ingredients']) and
                re.match(r"^.+$", r_json['order']['_id']) and
                r_json['order']['owner']['name'] == user_data['name'] and
                r_json['order']['owner']['email'] == user_data['email'] and
                time in r_json['order']['owner']['createdAt'] and
                time in r_json['order']['owner']['updatedAt'] and
                r_json['order']['status'] == 'done' and
                r_json['order']['name'] == data['name'] and
                time in r_json['order']['createdAt'] and
                time in r_json['order']['updatedAt'] and
                type(r_json['order']['number']) == int and
                r_json['order']['price'] == Halper.calculate_price(data['body']['ingredients']))

    @allure.title('Созданеие заказа - неавторизованный пользователь - успешное создание заказа')
    @pytest.mark.parametrize('data', DataOrder.dataset_ingredients)
    def test_order_unauthorized_user_successful_order(self, data):
        response = requests.post(f'{URL}{DataOrder.endpoint}', data=data['body'])
        r_json = response.json()

        assert (response.status_code == 200 and
                r_json['success'] == True and
                r_json['name'] == data['name'] and
                type(r_json['order']['number']) == int)

    @allure.title('Созданеие заказа - несуществующий ингредиент - ошибка сервера')
    def test_order_invalid_ingredient_hash_internal_server_error(self, authorize_user):
        headers = {'Authorization': authorize_user.json()['accessToken']}
        data = {"ingredients": ["61c0c5a71d1f852001bdaaa6c"]}
        response = requests.post(f'{URL}{DataOrder.endpoint}', headers=headers, data=data)

        assert response.status_code == 500

    @allure.title('Создание заказа - без ингредиентов - ошибка Ingredient ids must be provided')
    def test_order_without_ingredients_error_400(self, authorize_user):
        headers = {'Authorization': authorize_user.json()['accessToken']}
        data = {"ingredients": []}
        response = requests.post(f'{URL}{DataOrder.endpoint}', headers=headers, data=data)

        assert response.status_code == 400 and response.json() == DataOrder.error_order_without_ingredients

    @allure.title('Получение заказов конкретного пользователя - пользователь авторизовн - успешное получение списка')
    def test_orders_get_order_data_with_authorization_successful(self, authorize_user, create_order):
        headers = {'Authorization': authorize_user.json()['accessToken']}
        response = requests.get(f'{URL}{DataOrder.endpoint}', headers=headers)
        r_json = response.json()

        time, data, order = create_order
        order = order.json()

        assert (response.status_code == 200 and
                r_json['success'] == True and
                r_json['orders'][-1]['_id'] == order['order']['_id'] and
                r_json['orders'][-1]['ingredients'] == data['ingredients'] and
                r_json['orders'][-1]['status'] == 'done' and
                r_json['orders'][-1]['name'] == 'Бессмертный бургер' and
                time in r_json['orders'][-1]['createdAt'] and
                time in r_json['orders'][-1]['updatedAt'] and
                r_json['orders'][-1]['number'] == order['order']['number'] and
                type(r_json['total']) == int and
                type(r_json['totalToday']) == int)

    @allure.title('Получение заказов конкретного пользователя - пользователь авторизовн - успешное получение списка')
    def test_orders_get_order_data_without_authorization_error_401(self, create_order):
        response = requests.get(f'{URL}{DataOrder.endpoint}')

        assert (response.status_code == 401 and
                response.json() == DataOrder.error_unauthorized_user)

