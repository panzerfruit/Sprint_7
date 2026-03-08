import random
import string

def generate_random_string(length=10): # Функция для генерации случайной строки заданной длины
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_new_courier_data(): # Функция для получения данных нового курьера с уникальными значениями
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }