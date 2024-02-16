from collections import UserDict
from datetime import date, datetime
import re

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.__value)
        

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 0:
            self.__value = value
        else:
            raise ValueError

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError

# я тут пропоную свою реалізацыю якщо шо feel free щось міняти
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_val = datetime.strptime(re.sub(r'-', ' ', value), '%Y %m %d')

        if isinstance(new_val, date):
            self.__value = new_val.date()
        else:
            raise ValueError

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    min_len = 0

    def add_record(self, record: Record):
        try:
            self.data[record.name.value] = record   
        except ValueError:
            print('Failed to add the record!')

    def find(self, name):
        return self.data[name] if name in self.data else None

    def delete(self, name):
        self.data.pop(name) if name in self.data else None

    def __iter__(self):
        return self

    # Shows entire list
    def __next__(self):
        if self.min_len == len(self.data.values()):
            raise StopIteration
        else:
            value = list(self.data.values())[self.min_len]
            self.min_len += 1

            return value

    # Shows certain amount of pages
    def custom_iterator(self, end):
        while end+self.min_len <= len(self.data.values()):
            string_view = ''
            result = list(self.data.values())[self.min_len:end+self.min_len]
            for i in result:
                string_view += f'{i}\n'
            
            yield string_view
            
            self.min_len += end+self.min_len

        raise StopIteration