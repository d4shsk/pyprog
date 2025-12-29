import sqlite3
from myapp.models.currency import Currency
from myapp.models.user import User

class DatabaseController:
    def __init__(self):
        # Подключаемся к БД в памяти
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()
        self.seed_db() # Заполняем начальными данными

    def init_db(self):
        """Создание таблиц"""
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL,
                nominal INTEGER
            );
            
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
        """)
        self.conn.commit()

    def seed_db(self):
        """Заполнение тестовыми данными"""
        # Валюты
        currencies = [
            ("840", "USD", "Доллар США", 90.50, 1),
            ("978", "EUR", "Евро", 98.10, 1),
            ("392", "JPY", "Йена", 0.60, 100)
        ]
        self.cursor.executemany(
            "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES(?, ?, ?, ?, ?)", 
            currencies
        )
        
        # Пользователи
        users = [("Алексей",), ("Мария",), ("Дмитрий",)]
        self.cursor.executemany("INSERT INTO user(name) VALUES(?)", users)
        
        # Подписки (Алексей -> USD, Мария -> EUR)
        subs = [(1, 1), (2, 2)] 
        self.cursor.executemany("INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)", subs)
        
        self.conn.commit()

    # --- CRUD для Currency ---
    
    def get_all_currencies(self):
        self.cursor.execute("SELECT * FROM currency")
        rows = self.cursor.fetchall()
        # Преобразуем кортежи БД в объекты моделей
        return [Currency(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]

    def add_currency(self, num_code, char_code, name, value, nominal):
        sql = "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES(?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (num_code, char_code, name, value, nominal))
        self.conn.commit()

    def delete_currency(self, currency_id):
        sql = "DELETE FROM currency WHERE id = ?"
        self.cursor.execute(sql, (currency_id,))
        self.conn.commit()

    def update_currency_value(self, char_code, new_value):
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        self.cursor.execute(sql, (new_value, char_code))
        self.conn.commit()

    # --- Методы для Users ---
    
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM user")
        return [User(row[0], row[1]) for row in self.cursor.fetchall()]

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1])
        return None

    def get_user_subscriptions(self, user_id):
        """Получить валюты, на которые подписан пользователь (JOIN)"""
        sql = """
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """
        self.cursor.execute(sql, (user_id,))
        rows = self.cursor.fetchall()
        return [Currency(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]