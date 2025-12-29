import unittest
import sys
import os
from jinja2 import Environment, FileSystemLoader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp.controllers import author_controller, user_controller
from myapp.models.user import User

class TestControllersAndTemplates(unittest.TestCase):
    
    def setUp(self):
        """Подготовка: инициализация Jinja2 окружения вручную для тестов"""
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'myapp', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    # --- ТЕСТЫ КОНТРОЛЛЕРОВ ---
    
    def test_author_context(self):
        """Проверяем данные, которые готовит контроллер /author"""
        context = author_controller.author_context()
        self.assertIn('author', context)
        self.assertIn('app', context)
        self.assertEqual(context['author'].name, "Даниил Шарманов")
        self.assertEqual(context['app'].name, "CurrencyViewer")

    def test_user_detail_context_found(self):
        """Проверка контроллера user?id=1 (существующий)"""
        # Предполагаем, что в базе есть User с id=1
        context = user_controller.user_detail_context(1)
        self.assertIsNotNone(context)
        self.assertEqual(context['user'].id, 1)

    def test_user_detail_context_not_found(self):
        """Проверка контроллера user?id=999 (несуществующий)"""
        context = user_controller.user_detail_context(999)
        self.assertIsNone(context)

    # --- ТЕСТЫ ШАБЛОНОВ ---

    def test_template_users_render(self):
        """Проверка рендеринга users.html (циклы)"""
        template = self.env.get_template("users.html")
        
        # Подсовываем тестовые данные
        fake_users = [User(100, "TestUser1"), User(101, "TestUser2")]
        rendered_html = template.render(users=fake_users, title="Tests")
        
        # Проверяем, что имена попали в HTML
        self.assertIn("TestUser1", rendered_html)
        self.assertIn("TestUser2", rendered_html)
        self.assertIn("href=\"/user?id=100\"", rendered_html)

    def test_template_user_detail_conditions(self):
        """Проверка условий в user_detail.html (есть подписки / нет подписок)"""
        template = self.env.get_template("user_detail.html")
        
        # Случай 1: Нет подписок
        fake_user = User(1, "LonelyUser")
        html_empty = template.render(user=fake_user, subscriptions=[], title="Test")
        self.assertIn("Нет активных подписок", html_empty)
        
        # Случай 2: Есть подписки
        # Нам нужен объект похожий на Currency, используем Mock или просто класс
        class MockCurrency:
            char_code = "USD"
            name = "Dollar"
            value = 90.0
        
        html_subs = template.render(user=fake_user, subscriptions=[MockCurrency()], title="Test")
        self.assertIn("USD", html_subs)
        self.assertNotIn("Нет активных подписок", html_subs)

if __name__ == '__main__':
    unittest.main()