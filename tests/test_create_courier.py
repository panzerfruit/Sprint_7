import allure
import pytest
import requests
from data import Urls
from helpers import get_new_courier_data

class TestCreateCourier: # Тесты для создания курьера

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, delete_courier): # Тест на успешное создание курьера
        payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
        delete_courier.append(payload) # Добавляем данные курьера в список для удаления после теста
        response = requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера
        assert response.status_code == 201 # Проверяем, что статус код 201 (Created)
        assert response.json() == {"ok": True} # Проверяем, что в ответе есть поле "ok" со значением True

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, delete_courier): # Тест на ошибку при попытке создать курьера с уже существующим логином
        payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
        delete_courier.append(payload) # Добавляем данные курьера в список для удаления после теста
        requests.post(Urls.CREATE_COURIER, data=payload) # Создаем курьера с данными
        response = requests.post(Urls.CREATE_COURIER, data=payload) # Пытаемся создать курьера с теми же данными еще раз
        assert response.status_code == 409 # Проверяем, что статус код 409 (Conflict)
        assert "Этот логин уже используется" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Этот логин уже используется"

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_fails(self, missing_field): # Тест на ошибку при попытке создать курьера без одного из обязательных полей
        payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
        payload.pop(missing_field) # Удаляем одно из обязательных полей из данных курьера
        response = requests.post(Urls.CREATE_COURIER, data=payload) # Пытаемся создать курьера с неполными данными
        assert response.status_code == 400 # Проверяем, что статус код 400 (Bad Request)
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Недостаточно данных для создания учетной записи"