import allure
import requests
from data import Urls

class TestOrderList: # Тесты для получения списка заказов

    @allure.title("Получение списка заказов")
    def test_get_order_list(self): # Тест на получение списка заказов и проверку его структуры
        response = requests.get(Urls.ORDERS) # Отправляем запрос на получение списка заказов
        assert response.status_code == 200 # Проверяем, что статус код 200 (OK)
        assert type(response.json().get("orders")) == list # Проверяем, что в ответе есть поле "orders" и оно является списком
        assert len(response.json().get("orders")) > 0 # Проверяем, что список заказов не пустой, что означает наличие хотя бы одного заказа в системе