import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp.utils.currencies_api import get_currencies
# Если вы используете requests или urllib, их нужно мокать.
# Если у вас зашитая строка XML (как в прошлом примере), тестируем парсинг этой строки.

class TestCurrencyAPI(unittest.TestCase):

    def test_get_currencies_returns_list(self):
        """Проверка, что функция возвращает список и данные корректны"""
        currencies = get_currencies()
        self.assertIsInstance(currencies, list)
        self.assertGreater(len(currencies), 0)
        
        # Проверяем первый элемент
        first = currencies[0]
        self.assertTrue(hasattr(first, 'char_code'))
        self.assertTrue(hasattr(first, 'value'))
        self.assertIsInstance(first.value, float)

    # Пример сложного теста: имитация поломки XML (если бы функция читала извне)
    @patch('xml.etree.ElementTree.fromstring')
    def test_bad_xml_handling(self, mock_xml):
        """Имитация ошибки парсинга XML"""
        mock_xml.side_effect = Exception("Invalid XML")
        
        with self.assertRaises(Exception):
            # Здесь мы ожидаем, что функция get_currencies упадет, 
            # либо вы должны обработать это внутри функции и вернуть пустой список.
            # Если в коде нет try/except, тест должен ловить Exception.
            get_currencies()

if __name__ == '__main__':
    unittest.main()