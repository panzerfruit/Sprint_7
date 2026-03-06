class Urls:
    BASE_URL = "https://qa-scooter.praktikum-services.ru" # Базовый URL для API
    CREATE_COURIER = f"{BASE_URL}/api/v1/courier" # URL для создания курьера
    LOGIN_COURIER = f"{BASE_URL}/api/v1/courier/login" # URL для входа курьера
    ORDERS = f"{BASE_URL}/api/v1/orders" # URL для работы с заказами

class OrderData:
    BASE_ORDER = { # Базовые данные для создания заказа
        "firstName": "Leon",
        "lastName": "Kennedy",
        "address": "Racoon city, 32 st.",
        "metroStation": 4,
        "phone": "+7 800 555 35 55",
        "rentTime": 5,
        "deliveryDate": "2026-06-06",
        "comment": "Where's everyone going? Bingo?",
        "color": []
    }