import allure
import pytest
import requests
from constants import Constants

class TestCreateOrder:
    @allure.title("Проверка, что заказ создается")
    @pytest.mark.parametrize("color,result", [([-1], "GRAY"),
                                              ([-1], "BLACK"),
                                              ([-1], ["GRAY", "BLACK"]),
                                              ([-1], None)])
    def test_create_order(self, color, result):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": "4",
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        response = requests.post(Constants.CREATE_ORDER_URL, json=payload)
        assert response.status_code == 201 and response.json()['track'] is not None
