from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    ...
    # реалізація класу

class Phone(Field):
    ...
    # реалізація класу

class Birthday(Field):
    ...
     # реалізація класу
    
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def days_to_birthday(self): #Треба додати взаємодію з Birthday
        if self.birthday:
            ...
        else:
            ...

    def add_phone(self, phone):
        self.phone = Phone(phone)
        self.phones.append(self.phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

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
    def show_all_notes(self):
        return self.notes.data