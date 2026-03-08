import allure
import pytest
import requests
from data import Urls

class TestLoginCourier: # Тесты для логина курьера

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, create_courier_for_login): # Тест на успешную авторизацию курьера с правильными данными, используя данные курьера, созданного в фикстуре
        with allure.step("Подготавливаем валидные данные для входа"):
            payload = create_courier_for_login # Получаем данные курьера из фикстуры, который уже создан и готов для логина
            login_data = {"login": payload["login"], "password": payload["password"]} # Данные для логина, взятые из данных созданного курьера
        with allure.step("Отправляем запрос на авторизацию"):
            response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с правильными данными
        with allure.step("Проверяем успешный статус-код и получение id"):
            assert response.status_code == 200 # Проверяем, что статус код 200 (OK)
            assert "id" in response.json() # Проверяем, что в ответе есть поле "id", что означает успешный вход и получение ID курьера

    @allure.title("Ошибка логина с неправильным паролем")
    def test_login_wrong_password_fails(self, create_courier_for_login): # Тест на ошибку при попытке логина курьера с неправильным паролем
        with allure.step("Подготавливаем данные с неверным паролем"):
            payload = create_courier_for_login # Получаем данные курьера из фикстуры, который уже создан и готов для логина
            login_data = {"login": payload["login"], "password": "wrongpassword"} # Данные для логина с неправильным паролем
        with allure.step("Отправляем запрос на авторизацию"):
            response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с неправильным паролем
        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert response.status_code == 404 # Проверяем, что статус код 404 (Not Found), так как курьер с такими данными не найден
            assert "Учетная запись не найдена" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Учетная запись не найдена"

    @allure.title("Ошибка авторизации курьера при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fails(self, create_courier_for_login, missing_field): # Тест на ошибку при попытке логина курьера с данными, в которых отсутствует одно из обязательных полей (логин или пароль)
        with allure.step(f"Удаляем обязательное поле '{missing_field}' из данных авторизации"):
            payload = create_courier_for_login # Получаем данные курьера из фикстуры, который уже создан и готов для логина
            login_data = {"login": payload["login"], "password": payload["password"]}  # Данные для логина с правильными данными
            login_data.pop(missing_field) # Удаляем одно из обязательных полей (логин или пароль) из данных для логина
        with allure.step("Отправляем запрос на авторизацию с неполными данными"):
            response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с неполными данными
        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert response.status_code == 400 # Проверяем, что статус код 400 (Bad Request), так как данные для логина неполные
            assert "Недостаточно данных для входа" in response.json().get("message", "") # Проверяем, что в сообщении об ошибке есть текст "Недостаточно данных для входа"

    @allure.title("Авторизация под несуществующим пользователем")
    def test_login_nonexistent_user_fails(self): # Тест на ошибку при попытке логина курьера с данными, которых нет в системе
        with allure.step("Подготавливаем данные несуществующего курьера"):
            login_data = {"login": "iamtheonewhoknocks1337", "password": "password"} # Данные для логина с несуществующим логином
        with allure.step("Отправляем запрос на авторизацию"):
            response = requests.post(Urls.LOGIN_COURIER, data=login_data) # Отправляем запрос на логин курьера с несуществующими данными
        with allure.step("Проверяем статус-код и сообщение об ошибке"):
            assert response.status_code == 404 # Проверяем, что статус код 404 (Not Found), так как курьер с такими данными не найден