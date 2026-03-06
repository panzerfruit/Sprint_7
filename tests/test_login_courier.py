import allure
import pytest
import requests
from data import Urls
from helpers import get_new_courier_data

class TestLoginCourier: # Тесты для логина курьера

    @pytest.fixture(autouse=True)
    def setup(self, delete_courier): # Фикстура для подготовки данных курьера перед тестами и их удаления после
        self.payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
        requests.post(Urls.CREATE_COURIER, data=self.payload) # Создаем курьера с этими данными для тестов входа
        delete_courier.append(self.payload) # Добавляем данные курьера в список для удаления после тестов

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self): # Тест на успешный логин курьера с правильными данными
        login_data = {"login": self.payload["login"], "password": self.payload["password"]} # Данные для логина, взятые из данных созданного курьера
        response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с правильными данными
        assert response.status_code == 200 # Проверяем, что статус код 200 (OK)
        assert "id" in response.json() # Проверяем, что в ответе есть поле "id", что означает успешный вход и получение ID курьера

    @allure.title("Ошибка логина с неправильным паролем")
    def test_login_wrong_password_fails(self): # Тест на ошибку при попытке логина курьера с неправильным паролем
        login_data = {"login": self.payload["login"], "password": "wroooooonggpassword"} # Данные для логина с правильным логином, но неправильным паролем
        response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с неправильным паролем
        assert response.status_code == 404 # Проверяем, что статус код 404 (Not Found), так как курьер с такими данными не найден
        assert "Учетная запись не найдена" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Учетная запись не найдена"

    @allure.title("Ошибка при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, missing_field): # Тест на ошибку при попытке логина курьера без одного из обязательных полей
        login_data = {"login": self.payload["login"], "password": self.payload["password"]} # Данные для логина с правильными данными
        login_data.pop(missing_field) # Удаляем одно из обязательных полей из данных для логина
        response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с неполными данными
        assert response.status_code == 400 # Проверяем, что статус код 400 (Bad Request), так как данные для логина неполные
        assert "Недостаточно данных для входа" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Недостаточно данных для входа"

    @allure.title("Авторизация под несуществующим пользователем")
    def test_login_nonexistent_user_fails(self): # Тест на ошибку при попытке логина курьера с данными, которых нет в системе
        login_data = {"login": "iamtheonewhoknocks1337", "password": "password"} # Данные для логина с несуществующим логином
        response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с несуществующими данными
        assert response.status_code == 404 # Проверяем, что статус код 404 (Not Found), так как курьер с такими данными не найден