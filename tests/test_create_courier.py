import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants



class TestCreateCourier():
    @classmethod
    def setup_class(cls):
        cls.courier_data = {
            'login': faker.user_name(),
            'password': faker.password(),
            'firstName': faker.first_name()
        }

    def teardown_class(cls):
        login_payload = {
            'login': cls.courier_data['login'],
            'password': cls.courier_data['password']
        }
        response = requests.post(Constants.LOGIN_C0URIER_URL, json=login_payload)
        courier_id = response.json()['id']
        requests.delete(f"{Constants.DELETE_COURIER_URL}{courier_id}")

    @allure.title("Проверка, что курьера можно создать")
    def test_create_courier_OK(self):
        payload = self.courier_data
        response = requests.post(Constants.CREATE_COURIER_URL, json=payload)
        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Проверка, что если одного логина, запрос возвращает ошибку")
    def test_without_login_error(self):
        payload = {
            'login': '',
            'password': faker.password(),
            'firstName': faker.first_name()
        }
        response = requests.post(Constants.CREATE_COURIER_URL, json=payload)
        assert response.status_code == 400 and response.json() == {"code": 400,
    "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Проверка, что если нет пароля, запрос возвращает ошибку")
    def test_without_password_error(self):
        payload = {
            'login': faker.user_name(),
            'password': '',
            'firstName': faker.first_name()
        }
        response = requests.post(Constants.CREATE_COURIER_URL, json=payload)
        assert (response.status_code == 400 and response.json()
                == {"code": 400,
    "message": "Недостаточно данных для создания учетной записи"})

    @allure.title("Проверка, что если нет имени, запрос возвращает ошибку")
    def test_test_without_firstName_error(self):
        payload = {
                'login': faker.user_name(),
                'password': faker.password(),
                'firstName': ''
            }
        response = requests.post(Constants.CREATE_COURIER_URL, json=payload)
        assert (response.status_code == 400 and response.json()
                == {"code": 400,
    "message": "Недостаточно данных для создания учетной записи"})


    @allure.title("Проверка, что нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):
        payload_1 = self.courier_data
        requests.post(Constants.CREATE_COURIER_URL, json=payload_1)

        payload_2 = self.courier_data
        response_2 = requests.post(Constants.CREATE_COURIER_URL, json=payload_2)

        assert response_2.status_code == 409 and response_2.json() == {"code": 409,
        "message": "Этот логин уже используется. Попробуйте другой."}
