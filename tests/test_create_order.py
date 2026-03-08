import allure
import pytest
import requests
from data import Urls
from helpers import get_new_courier_data

class TestCreateOrder:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, delete_courier): # Тест на успешное создание курьера с правильными данными
        with allure.step("Подготавливаем данные для нового курьера"):
            payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
            delete_courier.append(payload) # Добавляем данные курьера в список для удаления после теста
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера с этими данными
        with allure.step("Проверяем успешный статус-код и тело ответа"):
            assert response.status_code == 201 # Проверяем, что статус код 201 (Created)
            assert response.json() == {"ok": True} # Проверяем, что в ответе есть поле "ok" со значением True, что означает успешное создание курьера

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, delete_courier): # Тест на ошибку при попытке создать курьера с данными, которые уже существуют в системе
        with allure.step("Подготавливаем данные и создаем первого курьера"):
            payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
            delete_courier.append(payload) # Добавляем данные курьера в список для удаления после теста
            requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера с этими данными для первого курьера
        with allure.step("Отправляем запрос на создание дубликата с теми же данными"):
            response = requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера с теми же данными для второго курьера
        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert response.status_code == 409 # Проверяем, что статус код 409 (Conflict), так как курьер с такими данными уже существует
            assert "Этот логин уже используется" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Этот логин уже используется"

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_fails(self, missing_field): # Тест на ошибку при попытке создать курьера без одного из обязательных полей
        with allure.step(f"Подготавливаем данные и удаляем поле '{missing_field}'"):
            payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
            payload.pop(missing_field) # Удаляем одно из обязательных полей из данных для создания курьера
        with allure.step("Отправляем запрос на создание курьера с неполными данными"):
            response = requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера с неполными данными
        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert response.status_code == 400 # Проверяем, что статус код 400 (Bad Request), так как данные для создания курьера неполные
            assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Недостаточно данных для создания учетной записи"