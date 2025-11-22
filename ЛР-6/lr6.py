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