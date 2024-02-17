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


class TegNote(Field):
    def __init__(self, value=None):
        super().__init__(value)


class BodyOfNote(Field):
    def __init__(self, value):
        super().__init__(value)


class Notes(UserDict):
    def __init__(self, body_of_note, teg=None):
        super().__init__()
        self.count = 0
        self.teg = TegNote(teg)
        self.text = BodyOfNote(body_of_note)

    def __str__(self):
        return f"Note {self.count}: /n {self.teg} /n {self.text}"
    
    def add_note(self):
        self.count += 1
        self.data[self.count] = [self.teg, self.text]

    def find_note(self, word: str, idx=None):
        if idx is None:
            for key, value in self.data.items():
                if value[0].find(word) != -1 or value[1].find(word) != -1:
                    return self.data[key]
                else:
                    continue
        else:
            return self.data[idx]
        
    def delete_note(self, word: str, idx=None):
        if idx is None:
            for key, value in self.data.items():
                if value[0].find(word) != -1 or value[1].find(word) != -1:
                    return self.data.pop(key)
                else:
                    continue
        else:
            return self.data.pop(idx)
        
    def edite_note(self, idx, new_text: str):
        self.data[idx] = new_text
        return self.data[idx]

    def add_note_teg(self, idx, teg: str):
        if self.data[idx][0] is None:
            self.data[idx][0] = teg
        else:
            return f'Notes nr.{idx} have a tags. You must change it.'

    def sort_not_for_teg(self):
        pass

   
class AddressBook(UserDict):
    ...
    # реалізація класу