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
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def days_to_birthday(self): #Треба додати взаємодію з Birthday
        if self.birthday:
            modified_date = self.birthday.value.replace(year=date.today().year + 1) \
            if self.birthday.value.month == 1 \
            else self.birthday.value.replace(year=date.today().year)
        
            result = modified_date - date.today()

            return result
        else:
            return f'No B Day :('
        
    def add_phone(self, phone):
        self.phone = Phone(phone)
        self.phones.append(self.phone)

    def add_birthday(self, date):
        try:
            self.birthday = Birthday(date)  
        except ValueError:
            print('Wrong date format! Enter the date in format year-month-day!')

    def remove_phone(self, phone):
        if phone in [p.value for p in self.phones]:
            for p in self.phones:
                if p.value == phone:
                    self.phones.remove(p)
                    break
        else:
            raise ValueError

    def edit_phone(self, old_phone, new_phone):
        if str(old_phone) not in [p.value for p in self.phones]:
            raise ValueError
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        
    def find_phone(self, phone):
        phone = str(phone)
        if phone in [p.value for p in self.phones]:
            return Phone(phone)
        else:
            return None
         
    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones) if self.phones else None}, "
                f"birthday: {self.birthday.value if self.birthday else None}")
   
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

if __name__ == '__main__':
    book = AddressBook()

    # Creating a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("1994-01-20")
    print(john_record)

    # Adding John's record to address book
    book.add_record(john_record)