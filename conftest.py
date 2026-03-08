import pytest
import requests
from data import Urls
from helpers import get_new_courier_data

@pytest.fixture
def delete_courier(): # Фикстура для удаления курьеров после тестов
    couriers_to_delete = []

    yield couriers_to_delete # Перед тестом предоставляем пустой список для хранения данных курьеров, которых нужно удалить

    for courier in couriers_to_delete: # После тестов проходим по списку курьеров и удаляем их
        login_resp = requests.post(Urls.LOGIN_COURIER, data=courier) # Отправляем запрос на вход курьера, чтобы получить его ID для удаления
        if login_resp.status_code == 200: # Если вход успешный, получаем ID курьера и удаляем его
            courier_id = login_resp.json().get("id") # Получаем ID курьера из ответа на вход
            requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}") # Отправляем запрос на удаление курьера по его ID

@pytest.fixture
def create_courier_for_login(delete_courier): # Фикстура создает курьера для тестов логина и возвращает его данные
    payload = get_new_courier_data() # Получаем данные нового курьера с уникальными значениями
    requests.post(Urls.CREATE_COURIER, data=payload) # Отправляем запрос на создание курьера с этими данными
    delete_courier.append(payload) # Передаем в фикстуру очистки, чтобы удалить после теста
    return payload # Возвращаем данные созданного курьера для использования в тестах логина