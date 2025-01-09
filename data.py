from halper import Halper


URL = 'https://stellarburgers.nomoreparties.site'

random_user_data = Halper.unique_user_data()


class DataRegister:
    endpoint = '/api/auth/register'

    # Набор данных для проверки обязательных полей
    dataset_fields = [
        {'name': Halper.unique_user_data()['name'], 'email': Halper.unique_user_data()['email']},
        {'name': Halper.unique_user_data()['name'], 'email': Halper.unique_user_data()['email'], 'password': ''},
        {'name': Halper.unique_user_data()['name'], 'password': Halper.unique_user_data()['password']},
        {'name': Halper.unique_user_data()['name'], 'email': '', 'password': Halper.unique_user_data()['password']},
        {'email': Halper.unique_user_data()['email'], 'password': Halper.unique_user_data()['password']},
        {'name': '', 'email': Halper.unique_user_data()['email'], 'password': Halper.unique_user_data()['password']},
    ]

    #  Ответ на регистрацию уже существующего пользователя
    error_existing_user = {
        "success": False,
        "message": "User already exists"
    }
    #  Ответ на регистарцию без обязательных полей
    error_fields_missing = {
        "success": False,
        "message": "Email, password and name are required fields"
    }


class DataLogin:
    endpoint = '/api/auth/login'
    # Набор данных для проверки полей авторизации
    dataset_fields = [
        {'email': random_user_data['email']},
        {'email': random_user_data['email'], 'password': random_user_data['password'][:-1]},
        {'email': random_user_data['email'][:-10], 'password': random_user_data['password']},
        {'password': random_user_data['password']}
    ]
    #  Ответ на некорректную авторизацию
    error_incorrect_data = {
        "success": False,
        "message": "email or password are incorrect"
    }


class DataUser:
    endpoint = '/api/auth/user'

    new_email = Halper.unique_user_data()['email']
    new_name = Halper.unique_user_data()['name']

    # Набор данных для проверки изменения данных авторизованного пользователя
    dataset_successful_change_fields = [
        ({'name': new_name}, {'email': random_user_data['email'], 'name': new_name}),
        ({'email': new_email}, {'email': new_email, 'name': random_user_data['name']})
    ]

    # Набор данных для проверки изменения данных неавторизованного пользователя
    dataset_failed_change_fields = [
        ({'name': new_name}, {'email': random_user_data['email'], 'name': random_user_data['name']}),
        ({'email': new_email}, {'email': random_user_data['email'], 'name': random_user_data['name']})
    ]

    # Ответ на смену данных пользователя без токена авторизации
    error_change_user_data = {
        "success": False,
        "message": "You should be authorised"
    }


class DataOrder:
    endpoint = '/api/orders'

    dataset_ingredients = [
        {
            'body':
                {"ingredients": ["61c0c5a71d1f82001bdaaa6f"]},
            'name': 'Бессмертный бургер'
        },
        {
            'body':
                {"ingredients": ["61c0c5a71d1f82001bdaaa6c", "61c0c5a71d1f82001bdaaa75", "61c0c5a71d1f82001bdaaa76",
                                 "61c0c5a71d1f82001bdaaa78"]},
            'name': 'Альфа-сахаридный антарианский краторный минеральный бургер'
         }
    ]

    #  Ответ на заказ без ингредиентов
    error_order_without_ingredients = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }

    #  Ответ на получение списка заказов без токена авторизации
    error_unauthorized_user = {
        "success": False,
        "message": "You should be authorised"
    }
