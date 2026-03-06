import allure
import pytest
import requests
from data import Urls, OrderData
import copy

class TestCreateOrder:
    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", [ # Параметризация теста с разными вариантами цвета для заказа
        ["BLACK"], # Тест на создание заказа с цветом "BLACK"
        ["GREY"],  # Тест на создание заказа с цветом "GREY"
        ["BLACK", "GREY"],  # Тест на создание заказа с цветами "BLACK" и "GREY"
        [] # Тест на создание заказа без указания цвета (пустой список)
    ])
    def test_create_order_colors(self, color): # Тест на создание заказа с разными вариантами цвета, включая пустой
        payload = copy.deepcopy(OrderData.BASE_ORDER) # Создаем копию базовых данных для заказа, чтобы не изменять оригинал
        payload["color"] = color # Устанавливаем цвет из параметров теста
        response = requests.post(Urls.ORDERS, json=payload) # Отправляем запрос на создание заказа с данными, включая цвет
        assert response.status_code == 201 # Проверяем, что статус код 201 (Created)
        assert "track" in response.json() # Проверяем, что в ответе есть поле "track", что означает успешное создание заказа и получение его трек-номера