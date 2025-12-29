class Author:
    def __init__(self, name, group):
        self.name = name
        self.group = group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        self._name = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if not isinstance(value, str):
            raise TypeError("Группа должна быть строкой")
        self._group = value