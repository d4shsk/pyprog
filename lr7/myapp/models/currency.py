class Currency:
    def __init__(self, uid, num_code, char_code, name, value, nominal):
        self.id = uid
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        # Обработка формата "48,6178" -> 48.6178
        if isinstance(val, str):
            val = float(val.replace(',', '.'))
        if not isinstance(val, (int, float)):
            raise TypeError("Курс должен быть числом")
        self._value = val