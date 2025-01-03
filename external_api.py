import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')


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
        url = f"https://api.apilayer.com/fixer/latest?symbols=EUR,USD&base=RUB"
        payload = {}
        headers = {
            "apikey": api_key
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # Проверка на успешность запроса
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()

        if not data.get('success'):
            raise Exception(f"Error: {data['error']['type']}")

        return data


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
        if currency == 'RUB':
            return float(amount)

        # Получаем курсы валют
        exchange_rates = ExternalAPI.get_exchange_rates()

        # Конвертация в рубли
        if currency in exchange_rates["rates"]:
            return float(amount) / float(exchange_rates["rates"][currency])

    raise ValueError("Unsupported currency or missing operationAmount.")
