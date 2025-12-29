import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, PackageLoader, select_autoescape

# Импорт контроллеров
from controllers import author_controller, user_controller, currencies_controller

# 1. Настройка Jinja2
env = Environment(
    loader=PackageLoader("myapp", "templates"), # Пакет myapp, папка templates
    autoescape=select_autoescape(['html', 'xml'])
)

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def _render(self, template_name, context=None):
        """Вспомогательный метод для рендеринга и отправки ответа"""
        if context is None:
            context = {}
            
        try:
            template = env.get_template(template_name)
            html_content = template.render(**context)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Template Error: {e}")

    def do_GET(self):
        # Парсинг URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        # Маршрутизация (Routing)
        if path == "/":
            context = author_controller.index_context()
            self._render("index.html", context)
            
        elif path == "/author":
            context = author_controller.author_context()
            # Можно использовать index.html или создать отдельный
            self._render("index.html", context) 

        elif path == "/users":
            context = user_controller.users_list_context()
            self._render("users.html", context)

        elif path == "/user":
            user_id = query.get('id', [None])[0]
            if user_id:
                context = user_controller.user_detail_context(user_id)
                if context:
                    self._render("user_detail.html", context)
                else:
                    self.send_error(404, "User not found")
            else:
                self.send_error(400, "Missing user ID")

        elif path == "/currencies":
            context = currencies_controller.currencies_context()
            self._render("currencies.html", context)

        else:
            self.send_error(404, "Page Not Found")

def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}...")
    print(f"Перейдите по ссылке: http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Сервер остановлен.")

if __name__ == "__main__":
    run()