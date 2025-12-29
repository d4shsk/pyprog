import unittest
import sys
import os
from unittest.mock import MagicMock

# Фикс путей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp.controllers.currencies_controller import CurrenciesController
from myapp.models.currency import Currency

class TestCurrenciesControllerMock(unittest.TestCase):
    
    def test_get_currencies_context(self):
        """Тест получения списка валют с моком БД"""
        # 1. Создаем Mock для DatabaseController
        mock_db = MagicMock()
        
        # 2. Настраиваем поведение: метод get_all_currencies должен вернуть готовый список
        fake_list = [
            Currency(1, "840", "USD", "Test Dollar", 90.0, 1),
            Currency(2, "978", "EUR", "Test Euro", 100.0, 1)
        ]
        mock_db.get_all_currencies.return_value = fake_list
        
        # 3. Инициализируем контроллер с фейковой БД
        controller = CurrenciesController(mock_db)
        
        # 4. Вызываем метод
        context = controller.get_currencies_context()
        
        # 5. Проверяем результаты
        self.assertEqual(context['title'], "Список валют (из БД)")
        self.assertEqual(len(context['currencies']), 2)
        self.assertEqual(context['currencies'][0].char_code, "USD")
        
        # Проверяем, что контроллер действительно вызвал метод БД
        mock_db.get_all_currencies.assert_called_once()

    def test_delete_currency(self):
        """Тест вызова удаления"""
        mock_db = MagicMock()
        controller = CurrenciesController(mock_db)
        
        controller.delete(55)
        
        # Проверяем, что метод БД delete_currency был вызван с аргументом 55
        mock_db.delete_currency.assert_called_once_with(55)

if __name__ == '__main__':
    unittest.main()