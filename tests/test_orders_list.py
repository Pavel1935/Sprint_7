import allure
import requests
from constants import Constants

class TestGetOrders:
    @allure.title('Проверка что в тело ответа возвращается список заказов')
    def test_order_list(self):
        response = requests.get(Constants.GET_ORDERS_URL)
        assert response.status_code == 200 and response.json()['orders'] is not None