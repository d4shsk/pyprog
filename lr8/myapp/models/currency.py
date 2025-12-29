class Currency:
    def __init__(self, uid, num_code, char_code, name, value, nominal):
        self.id = uid
        self.num_code = num_code
        self.char_code = char_code 
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, val: str):
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self._char_code = val.upper()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        # Обработка строки с запятой, если пришла строка
        if isinstance(val, str):
            val = float(val.replace(',', '.'))
        
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self._value = val