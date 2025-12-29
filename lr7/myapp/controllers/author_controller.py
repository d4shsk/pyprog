from myapp.models.app import App
from myapp.models.author import Author

def index_context():
    author = Author("Даниил Шарманов", "1-1")
    app_info = App("CurrencyViewer", "1.0", author)
    return {
        "title": "Главная",
        "app": app_info,
        "author": author
    }

def author_context():
    author = Author("Даниил Шарманов", "1-1")
    app_info = App("CurrencyViewer", "1.0", author)
    
    return {
        "title": "Об авторе",
        "author": author,
        "app": app_info
    }