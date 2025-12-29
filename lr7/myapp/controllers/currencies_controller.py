from myapp.utils.currencies_api import get_currencies

# Кэшируем валюты, чтобы не парсить каждый раз (упрощение)
CACHED_CURRENCIES = get_currencies()

def get_all_currencies():
    return CACHED_CURRENCIES

def currencies_context():
    return {
        "title": "Курсы валют",
        "currencies": CACHED_CURRENCIES
    }