import os
import requests
from dotenv import load_dotenv
from utils import load_json_file
from utils import json

load_dotenv()

api_key = os.getenv("API_KEY")


# Модуль для работы с внешним API
class ExternalAPI:
    @staticmethod
    def get_exchange_rates():
        """
        Получает текущие курсы валют относительно рубля (RUB).

        :return: Словарь с текущими курсами валют, где ключи — это коды валют,
                 а значения — их курсы относительно рубля.
        :raises Exception: Если запрос к API не удался или если ответ не успешен.
        """
        url = "https://api.apilayer.com/fixer/latest?symbols=EUR,USD&base=RUB"
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers)  # Используем метод GET
            response.raise_for_status()  # Проверка на ошибки HTTP

            data = response.json()

            if not data.get("success"):
                raise Exception(f"Error: {data['error']['type']}")

            return data["rates"]  # Возвращаем только курсы валют

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при обращении к API: {e}")
        except json.JSONDecodeError:
            raise Exception("Ошибка декодирования ответа от API.")


# Функция для конвертации суммы в рубли
def convert_to_rub(data):
    """
    Конвертирует сумму транзакции в рубли.

    :param data: Словарь с данными о транзакции, должен содержать ключи:
                 'operationAmount' (содержит 'amount' и 'currency').
    :return: Сумма транзакции в рублях как float.
    :raises ValueError: Если валюта не поддерживается (не RUB, USD или EUR).
    """
    if "operationAmount" in data:
        amount = data["operationAmount"]["amount"]
        currency = data["operationAmount"]["currency"]["code"]

        # Если валюта уже в рублях, возвращаем сумму
        if currency == "RUB":
            return float(amount)

        # Получаем курсы валют
        try:
            exchange_rates = ExternalAPI.get_exchange_rates()
        except Exception as e:
            print(f"Не удалось получить курсы валют: {e}")
            return None  # Или можно вернуть 0.0 или другое значение по умолчанию

        # Конвертация в рубли
        if currency in exchange_rates:
            return float(amount) / float(exchange_rates[currency])

    raise ValueError("Unsupported currency or missing operationAmount.")


# Пример использования функции загрузки JSON и конвертации валюты
if __name__ == "__main__":
    transaction_data = load_json_file("transaction_data.json")  # Замените на ваш файл

    try:
        rub_amount = convert_to_rub(transaction_data)
        if rub_amount is not None:
            print(f"Сумма в рублях: {rub_amount:.2f} RUB")
    except ValueError as ve:
        print(f"Ошибка конвертации: {ve}")
