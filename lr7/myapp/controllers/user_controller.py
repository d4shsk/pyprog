from myapp.models.user import User
from myapp.models.user_currency import UserCurrency
from myapp.controllers.currencies_controller import get_all_currencies

# Имитация базы данных в памяти
users_db = [
    User(1, "Алексей"),
    User(2, "Мария"),
    User(3, "Дмитрий")
]

# Подписки: user_id -> list of currency_ids
subscriptions_db = [
    UserCurrency(1, 1, "R01235"), # Алексей -> USD
    UserCurrency(2, 2, "R01239"), # Мария -> EUR
]

def users_list_context():
    return {
        "title": "Список пользователей",
        "users": users_db
    }

def user_detail_context(user_id):
    try:
        user_id = int(user_id)
        user = next((u for u in users_db if u.id == user_id), None)
    except ValueError:
        user = None

    if not user:
        return None

    # Находим подписки пользователя
    user_subs = [s for s in subscriptions_db if s.user_id == user.id]
    all_currencies = get_all_currencies()
    
    # Собираем полные объекты валют для подписок
    subscribed_currencies = []
    for sub in user_subs:
        found = next((c for c in all_currencies if c.id == sub.currency_id), None)
        if found:
            subscribed_currencies.append(found)

    return {
        "title": f"Пользователь {user.name}",
        "user": user,
        "subscriptions": subscribed_currencies
    }