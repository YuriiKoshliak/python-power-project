# record.py
from datetime import datetime
from field import Field

class Name(Field):
    def valid(self, value):
        return value.isalpha()

class Phone(Field):
    def valid(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def valid(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Email(Field):
    def valid(self, value):
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(email_pattern.match(value))

class Record:
    def __init__(self, name, birthday=None, email=None):
        self.name = Name(name)
        self._email = None
        self.email = email
        self.phones = []
        self.birthday = Birthday(birthday) if birthday is not None else None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        email_field = Email(value)
        if email_field.valid(value):
            self._email = email_field.value
        else:
            raise ValueError("Invalid email address")

    # Другие методы класса Record

    def __str__(self):
        phones_str = '; '.join(str(phone.value) for phone in self.phones)
        return f"Contact name: {self.name.value}, email: {self.email}, phones: {phones_str}"
