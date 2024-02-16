class Field:
    def __init__(self, value):
        if not self.valid(value):
            raise ValueError("Incorrect value")
        self.__value = value

    def valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.valid(value):
            raise ValueError("Incorrect value")
        self.__value = value