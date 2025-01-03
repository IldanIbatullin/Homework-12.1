# test_utils.py
import unittest
from unittest.mock import mock_open, patch
from utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_load_empty_list(self, mock_file):
        """Тест загрузки пустого списка."""
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("dummy_path.json", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_invalid_json(self, mock_file):
        """Тест загрузки некорректного JSON."""
        with self.assertRaises(ValueError):
            load_transactions("dummy_path.json")
        mock_file.assert_called_once_with("dummy_path.json", encoding="utf-8")

    @patch("os.path.exists", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}]',
    )
    def test_load_valid_json(self, mock_file, mock_exists):
        """Тест загрузки корректного JSON."""
        result = load_transactions("dummy_path.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["operationAmount"]["amount"], "100")
        self.assertEqual(result[0]["operationAmount"]["currency"]["code"], "USD")
        mock_file.assert_called_once_with("dummy_path.json", encoding="utf-8")

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        """Тест на случай, если файл не найден."""
        with self.assertRaises(FileNotFoundError):
            load_transactions("dummy_path.json")


if __name__ == "__main__":
    unittest.main()
