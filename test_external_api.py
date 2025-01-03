import unittest
from unittest.mock import patch, MagicMock
from external_api import convert_to_rub, ExternalAPI


class TestExternalAPI(unittest.TestCase):

    @patch("external_api.requests.request")
    def test_get_exchange_rates_success(self, mock_request):
        """Тест успешного получения курсов валют."""
        # Настройка мок-ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {"USD": 75.0, "EUR": 85.0},
        }
        mock_request.return_value = mock_response

        rates = ExternalAPI.get_exchange_rates()
        self.assertEqual(rates["rates"]["USD"], 75.0)
        self.assertEqual(rates["rates"]["EUR"], 85.0)

    @patch("external_api.requests.request")
    def test_get_exchange_rates_failure(self, mock_request):
        """Тест обработки ошибки при получении курсов валют."""
        # Настройка мок-ответа с ошибкой
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        with self.assertRaises(Exception) as context:
            ExternalAPI.get_exchange_rates()

        self.assertTrue(
            "API request failed with status code 500" in str(context.exception)
        )

    @patch("external_api.ExternalAPI.get_exchange_rates")
    def test_convert_usd_to_rub(self, mock_get_exchange_rates):
        """Тест конвертации USD в RUB."""
        # Настройка возврата курсов валют
        mock_get_exchange_rates.return_value = {
            "success": True,
            "rates": {"USD": 75.0, "EUR": 85.0},
        }

        transaction = {
            "operationAmount": {"amount": "100", "currency": {"code": "USD"}}
        }

        result = convert_to_rub(transaction)
        self.assertAlmostEqual(result, 1333.33)  # 100 / (1/75.0)

    @patch("external_api.ExternalAPI.get_exchange_rates")
    def test_convert_eur_to_rub(self, mock_get_exchange_rates):
        """Тест конвертации EUR в RUB."""
        # Настройка возврата курсов валют
        mock_get_exchange_rates.return_value = {
            "success": True,
            "rates": {"USD": 75.0, "EUR": 85.0},
        }

        transaction = {
            "operationAmount": {"amount": "100", "currency": {"code": "EUR"}}
        }

        result = convert_to_rub(transaction)
        self.assertAlmostEqual(result, 1176.47)  # 100 / (1/85.0)

    def test_convert_rub(self):
        """Тест, когда валюта уже в RUB."""
        transaction = {
            "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}
        }

        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)  # Сумма в рублях должна остаться неизменной

    def test_unsupported_currency(self):
        """Тест на неподдерживаемую валюту."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "JPY"},  # Неподдерживаемая валюта
            }
        }

        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)

        self.assertTrue(
            "Unsupported currency or missing operationAmount." in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
