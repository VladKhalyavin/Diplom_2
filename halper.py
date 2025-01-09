import os
import json
import datetime
from faker import Faker
from typing import Dict, List


class Halper:

    @staticmethod
    def unique_user_data(password: int = 10) -> Dict:
        """
        Создает словарь с данными пользователя
        :param password: длинна пароля (по умолчанию 10 символов)
        :return: словарь данных пользователя с ключами 'name','email','password'
        """

        fake = Faker("ru_RU")
        return {'name': fake.user_name(),
                'email': fake.email(domain='yandex.ru'),
                'password': fake.password(password, False)}

    @staticmethod
    def get_ingredient_data(ingredient_id: str) -> Dict:
        """
        Возвращает информацию об ингредиенте по id ингредиента
        :param ingredient_id: значение _id ингредиента
        :return: Словарь с данными об ингредиенте
        """

        with open(f'{os.path.abspath("ingredients.json")}', 'r', encoding='utf-8') as file:
            ingredients = json.load(file)

        for ingredient in ingredients['data']:
            if ingredient_id in ingredient['_id']:
                return ingredient

    @staticmethod
    def collect_order(ingredients: list) -> List:
        """
        Создает спискок ингредиентов, аналогичный orders.ingredients
        :param ingredients: список хеш сумм ингредиентов. Пример: ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa75"]
        :return: Возвращает список
        """

        order_ingredients = []
        for ingredient in ingredients:
            order_ingredients.append(Halper.get_ingredient_data(ingredient))
        return order_ingredients

    @staticmethod
    def calculate_price(ingredients: list) -> int:
        """
        Считает суммарную стоимость иггредиентов бургера
        :param ingredients: список хеш сумм ингредиентов. Пример: ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa75"]
        :return: Возвращает суммарную стоимость
        """
        price = 0
        for ingredient in ingredients:
            price += Halper.get_ingredient_data(ingredient)['price']
        return price

    @staticmethod
    def get_time():
        """
        Создает строку с текущей доатой и временем. Пример: 2024-07-27T11:52
        """
        now = datetime.datetime.utcnow()
        date = [now.month, now.day, now.hour, now.minute]

        format_date = []

        for i in date:
            i = str(i)
            if len(i) < 2:
                i = f'0{i}'
            format_date.append(i)

        return f"{now.year}-{format_date[0]}-{format_date[1]}T{format_date[2]}:{format_date[3]}"


print(Halper.get_time())