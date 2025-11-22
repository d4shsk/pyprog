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