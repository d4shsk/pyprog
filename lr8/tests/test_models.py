import unittest
import sys
import os

# Добавляем путь к корню проекта, чтобы видеть пакет myapp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp.models.author import Author
from myapp.models.user import User
from myapp.models.currency import Currency

class TestModels(unittest.TestCase):

    def test_author_creation(self):
        """Проверка корректного создания автора"""
        author = Author("Даниил Шарманов", "1-1")
        self.assertEqual(author.name, "Даниил Шарманов")
        self.assertEqual(author.group, "1-1")

    def test_author_validation(self):
        """Проверка выброса исключений при некорректных типах"""
        # Проверяем, что имя не может быть числом
        with self.assertRaises(TypeError):
            Author(123, "1-1")
        
        # Проверяем, что группа не может быть числом
        with self.assertRaises(TypeError):
            Author("Name", 123)

    def test_currency_value_setter(self):
        """Проверка сеттера Value для валюты (конвертация строки с запятой)"""
        # Создаем валюту с заглушками, проверяем только value
        curr = Currency("R01", "840", "USD", "Доллар", 0, 1)
        
        # Тест передачи строки с запятой
        curr.value = "90,50" 
        self.assertEqual(curr.value, 90.50)
        
        # Тест передачи числа
        curr.value = 85.0
        self.assertEqual(curr.value, 85.0)

    def test_currency_validation(self):
        """Проверка валидации курса валют"""
        curr = Currency("R01", "840", "USD", "Доллар", 0, 1)
        with self.assertRaises(ValueError): 
            curr.value = "Not a number"

if __name__ == '__main__':
    unittest.main()