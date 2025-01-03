import json


def load_transactions(file_path):
    """
    Загружает данные о транзакциях из JSON-файла.

    :param file_path: Путь к JSON-файлу с данными о транзакциях.
    :return: Список словарей с данными о транзакциях, если файл существует и содержит список,
             иначе пустой список.
    :raises FileNotFoundError: Если файл не найден.
    :raises json.JSONDecodeError: Если файл содержит некорректные данные JSON.
    """
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)  # Загружаем данные из файла в формате JSON
    return data
