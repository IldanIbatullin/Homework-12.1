import json


def load_json_file(file_path):
    """
    Загружает данные из JSON-файла.

    :param file_path: Путь к файлу.
    :return: Содержимое файла как словарь, или пустой список в случае ошибки.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}. Возвращаем пустой список.")
        return []
    except json.JSONDecodeError:
        print(
            f"Ошибка декодирования JSON в файле: {file_path}. Возвращаем пустой список."
        )
        return []
