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
    def __init__(self):
        super().__init__()
        self.count = 0
        self.teg = ''
        self.text = ''

    def __str__(self):
        return f"Note {self.count}: /n {self.teg} /n {self.text}"
    
    def add_note(self, body_of_note, teg=None):
        self.count += 1
        self.teg = TegNote(teg)
        self.text = BodyOfNote(body_of_note)
        self.data[self.count] = [self.teg, self.text]
        return self.data[self.count]

    def find_note(self, idx: str):
        if idx.isdigit():
            return self.data.get(int(idx))
        else:
            for key, value in self.data.items():
                if str(value[0]).find(idx) != -1 or str(value[1]).find(idx) != -1:
                    return self.data.get(key)
                else:
                    continue
        
    def delete_note(self, idx: str):
        if idx.isdigit():
            return self.data.pop(int(idx))
        else:
            for key, value in self.data.items():
                if str(value[0]).find(idx) != -1 or str(value[1]).find(idx) != -1:
                    return self.data.pop(key)
                else:
                    continue
        
    def edite_note(self, idx, new_text: str):
        self.data[int(idx)] = new_text
        return self.data[int(idx)]

    def add_note_teg(self, idx, teg: str):
        if self.data.get(idx) == '':
            self.data[int(idx)][0] = teg
        else:
            return f'Notes nr.{idx} have a tags. You must change it.'

    def sort_note_for_teg(self):
        self.list_tegs = []
        for i in self.data.values():
            self.list_tegs.append(str(i[0]))
        self.list_tegs.sort()
        for n in self.list_tegs:
            for key, value in self.data.items():
                if str(value[0]) == str(n):
                    return self.data.get(key)
                else:
                    continue

   
class AddressBook(UserDict):
    def __init__(self):
        self.notes = Notes()
    
    def write_note(self, body_of_note, teg=None):
        return self.notes.add_note(body_of_note, teg)

    def add_teg_to_note(self, idx, teg):
        return self.notes.add_note_teg(idx,teg)

    def change_note(self, idx, text):
        return self.notes.edite_note(idx, text)

    def search_of_note(self, word):
        return self.notes.find_note(word)

    def sorting_of_notes(self):
        return self.notes.sort_note_for_teg()

    def delete_the_note(self, word):
        return self.notes.delete_note(word)

