import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from myapp.controllers.database_controller import DatabaseController
from myapp.controllers import author_controller
from myapp.controllers.user_controller import UserController
from myapp.controllers.currencies_controller import CurrenciesController

# Инициализация Jinja2
template_path = os.path.join(current_dir, 'templates')
env = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape(['html', 'xml'])
)

# --- ИНИЦИАЛИЗАЦИЯ БД И КОНТРОЛЛЕРОВ ---
db = DatabaseController()
curr_controller = CurrenciesController(db)
user_controller = UserController(db)
# ---------------------------------------

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def _render(self, template_name, context=None):
        if context is None: context = {}
        try:
            template = env.get_template(template_name)
            html_content = template.render(**context)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Template Error: {e}")

    def _redirect(self, path):
        """Вспомогательный метод для редиректа"""
        self.send_response(303)
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == "/":
            self._render("index.html", author_controller.index_context())

        elif path == "/author":
            self._render("index.html", author_controller.author_context())

        elif path == "/users":
            self._render("users.html", user_controller.users_list_context())

        elif path == "/user":
            uid = query.get('id', [None])[0]
            if uid:
                ctx = user_controller.user_detail_context(uid)
                if ctx:
                    self._render("user_detail.html", ctx)
                else:
                    self.send_error(404, "User not found")
            else:
                self.send_error(400, "Missing ID")

        elif path == "/currencies":
            self._render("currencies.html", curr_controller.get_currencies_context())

        # --- НОВЫЙ МАРШРУТ: УДАЛЕНИЕ ---
        elif path == "/currency/delete":
            cid = query.get('id', [None])[0]
            if cid:
                curr_controller.delete(cid)
                # После удаления возвращаемся на список
                self._redirect("/currencies")
            else:
                self.send_error(400, "ID missing for delete")
        # -------------------------------

        else:
            self.send_error(404, "Not Found")

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    run()