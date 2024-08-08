import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants


class TestLoginCourier():

    @classmethod
    def setup_class(cls):
        cls.courier_data = {
            'login': faker.user_name(),
            'password': faker.password(),
            'firstName': faker.first_name()
        }

        requests.post(Constants.CREATE_COURIER_URL, json=cls.courier_data)

    @classmethod
    def teardown_class(cls):
        login_payload = {
            'login': cls.courier_data['login'],
            'password': cls.courier_data['password']
        }
        response = requests.post(Constants.LOGIN_C0URIER_URL, json=login_payload)
        courier_id = response.json()['id']
        requests.delete(f"{Constants.DELETE_COURIER_URL}{courier_id}")

    @allure.title("Проверка что курьер может авторизоваться")
    def test_login_OK(self):
        payload = {
            'login': self.courier_data['login'],
            'password': self.courier_data['password']
        }
        response = requests.post(Constants.LOGIN_C0URIER_URL, json=payload)
        assert response.status_code == 200 and response.json()['id'] is not None

    @allure.title("Проверка что если если какого-то поля нет, запрос возвращает ошибку")
    def test_without_login_error(self):
        payload = {
            'password': self.courier_data['password']
        }
        response = requests.post(Constants.LOGIN_C0URIER_URL, json=payload)
        assert (response.status_code == 400 and response.json()
                == {"code": 400, "message": "Недостаточно данных для входа"})

    @allure.title("если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_exist_login_password_error(self):
        payload = {
            'login': faker.user_name(),
            'password': faker.password()
        }
        response = requests.post(Constants.LOGIN_C0URIER_URL, json=payload)
        assert (response.status_code == 404 and response.json()
                == {"code": 404, "message": "Учетная запись не найдена"})
