import pytest
import requests
from data import Urls

@pytest.fixture
def delete_courier(): # Фикстура для удаления курьеров после тестов
    couriers_to_delete = []

    yield couriers_to_delete # Перед тестом предоставляем пустой список для хранения данных курьеров, которых нужно удалить

    for courier in couriers_to_delete: # После тестов проходим по списку курьеров и удаляем их
        login_resp = requests.post(Urls.LOGIN_COURIER, data=courier) # Отправляем запрос на вход курьера, чтобы получить его ID для удаления
        if login_resp.status_code == 200: # Если вход успешный, получаем ID курьера и удаляем его
            courier_id = login_resp.json().get("id") # Получаем ID курьера из ответа на вход
            requests.delete(f"{Urls.CREATE_COURIER}/{courier_id}") # Отправляем запрос на удаление курьера по его ID