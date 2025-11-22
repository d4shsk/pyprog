# Лабораторная работа № 6

## Формулировка задания

Написать функцию `get_currencies(currency_codes, url)`, которая обращается к API (по умолчанию ЦБ РФ) и возвращает словарь курсов валют для валют из переданного списка.

**Требования:**

1.  Использовать библиотеку `requests`.
2.  Реализовать обработку ошибок (отсутствие данных, ошибки сети, отсутствие валюты в базе).
3.  В случае ошибки функция должна возвращать `None`.
4.  Итерация 1: Логирование через `print` (sys.stdout).
5.  Итерация 2: Вынос обработки ошибок в декоратор.
6.  Итерация 3: Использование модуля `logging` вместо `print`.

## Описание работы кода

В итоговой реализации объединены требования всех итераций с упором на финальную (Итерация 3).

1.  **Декоратор `error_handler`:**

      * Обертывает основную функцию.
      * Использует блок `try...except` для перехвата исключений.
      * Обрабатывает `requests.RequestException` (ошибки сети), `ValueError` (некорректные данные API) и `KeyError` (отсутствие валюты).
      * В случае возникновения исключения записывает сообщение в лог, используя модуль `logging` (уровень ERROR), и возвращает `None`.

2.  **Функция `get_currencies`:**

      * Выполняет GET-запрос к указанному URL.
      * Проверяет статус ответа (`response.raise_for_status()`).
      * Проверяет наличие ключа `Valute` в полученном JSON. Если ключа нет, выбрасывает `ValueError`.
      * Перебирает запрошенные коды валют. Если код отсутствует в ответе API, выбрасывает `KeyError`.
      * Формирует и возвращает словарь `{код: значение}`.

## Решение

```python
import requests
import logging
import functools
import sys
from typing import List, Dict, Optional

# Настройка логгера (Итерация 3)
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Декоратор для обработки ошибок (Итерация 2 + 3)
def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            # Обработка ошибки запроса к API
            logging.error(f"API Request Error: {e}")
            return None
        except ValueError as e:
            # Обработка логических ошибок (нет ключа Valute и т.д.)
            logging.error(f"Data Error: {e}")
            return None
        except KeyError as e:
             # Обработка отсутствия конкретной валюты
            logging.error(f"Currency missing error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None
    return wrapper

# Основная функция
@error_handler
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Optional[Dict[str, float]]:
    """
    Получает курс валют с заданного URL.
    """
    response = requests.get(url)
    
    # Если статус не 200, requests вызовет исключение, которое поймает декоратор
    response.raise_for_status()
    
    data = response.json()

    # Проверка: в ответе не содержатся курсы валют
    if 'Valute' not in data:
        raise ValueError("Response does not contain 'Valute' key")

    result = {}
    
    for code in currency_codes:
        # Проверка: в словаре нет валюты из списка
        if code not in data['Valute']:
            raise KeyError(f"Currency code '{code}' not found in response")
        
        result[code] = data['Valute'][code]['Value']

    return result

if __name__ == "__main__":
    import sys
    # Пример использования
    print("Тест 1: Корректный запрос")
    rates = get_currencies(['USD', 'EUR'])
    print(f"Result: {rates}\n")

    print("Тест 2: Несуществующая валюта")
    rates_error = get_currencies(['USD', 'ZZZ'])
    print(f"Result: {rates_error}\n")

    print("Тест 3: Некорректный URL")
    rates_url_error = get_currencies(['USD'], url="https://invalid-url.com/json")
    print(f"Result: {rates_url_error}\n")
```

## Проверка

Тестирование проводилось с помощью модуля `unittest` и `unittest.mock` для симуляции ответов API.

Сценарии тестов:  

1.  Успешный запрос: Функция возвращает правильный словарь с курсами.
2.  Ошибка API: Симуляция разрыва соединения. Проверяется, что функция возвращает `None` и в лог пишется "API Request Error".
3.  Некорректный JSON: Ответ сервера не содержит ключа `'Valute'`. Проверяется запись "Data Error".
4.  Отсутствующая валюта: Запрос валюты, которой нет в ответе ЦБ (например, 'ZZZ'). Проверяется запись "Currency missing error".

```python
import unittest
import logging
import sys
from unittest.mock import patch, Mock
from lr6 import get_currencies

class TestCurrencyFetcher(unittest.TestCase):

    def setUp(self):
        # Перехватываем вывод логов для проверки
        self.logger = logging.getLogger()
        self.log_capture_string = io.StringIO()
        self.ch = logging.StreamHandler(self.log_capture_string)
        self.ch.setLevel(logging.ERROR)
        self.logger.addHandler(self.ch)

    def tearDown(self):
        self.logger.removeHandler(self.ch)

    @patch('requests.get')
    def test_success(self, mock_get):
        """Проверка успешного получения данных"""
        # Имитируем ответ сервера
        mock_response = Mock()
        mock_response.json.return_value = {
            'Valute': {
                'USD': {'Value': 90.5},
                'EUR': {'Value': 98.2}
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_currencies(['USD', 'EUR'])
        
        self.assertEqual(result, {'USD': 90.5, 'EUR': 98.2})
        self.assertIn('USD', result)

    @patch('requests.get')
    def test_api_error(self, mock_get):
        """Проверка обработки ошибки запроса (404/Connection Error)"""
        # Имитируем ошибку сети
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        result = get_currencies(['USD'])
        
        self.assertIsNone(result)
        # Проверяем, что ошибка записалась в лог
        log_contents = self.log_capture_string.getvalue()
        self.assertIn("API Request Error", log_contents)

    @patch('requests.get')
    def test_missing_valute_key(self, mock_get):
        """Проверка случая, когда JSON не содержит ключа Valute"""
        mock_response = Mock()
        mock_response.json.return_value = {'Incorrect': 'Data'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_currencies(['USD'])

        self.assertIsNone(result)
        log_contents = self.log_capture_string.getvalue()
        self.assertIn("Response does not contain 'Valute' key", log_contents)

    @patch('requests.get')
    def test_missing_currency(self, mock_get):
        """Проверка отсутствия запрашиваемой валюты в ответе"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'Valute': {'USD': {'Value': 90.0}}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Запрашиваем USD (есть) и GBP (нет)
        result = get_currencies(['USD', 'GBP'])

        self.assertIsNone(result)
        log_contents = self.log_capture_string.getvalue()
        self.assertIn("Currency code 'GBP' not found", log_contents)

import io
import requests

if __name__ == '__main__':
    unittest.main()
```
