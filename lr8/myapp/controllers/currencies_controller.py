class CurrenciesController:
    def __init__(self, db_controller):
        self.db = db_controller

    def get_currencies_context(self):
        currencies = self.db.get_all_currencies()
        return {
            "title": "Список валют (из БД)",
            "currencies": currencies
        }

    def delete(self, currency_id):
        self.db.delete_currency(currency_id)