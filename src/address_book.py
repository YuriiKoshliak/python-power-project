# address_book.py
from collections import UserDict
import os
import pickle
from record import Record

class AddressBook(UserDict):
    def __init__(self, file=None):
        super().__init__()
        self.file = file

    def get_full_file_path(self):
        if self.file:
            return os.path.join(os.getcwd(), self.file)
        else:
            print("File not specified. Unable to get the full file path.")
            return None

    def iterator(self, n):
        values = list(self.data.values())
        for i in range(0, len(values), n):
            yield values[i:i + n]

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_address_book(self):
        if full_file_path := self.get_full_file_path():
            with open(full_file_path, "wb") as fh:
                pickle.dump(self.data, fh)
            print(f"Address book saved successfully to '{full_file_path}'.")

    def load_address_book(self):
        if full_file_path := self.get_full_file_path():
            if os.path.exists(full_file_path):
                with open(full_file_path, "rb") as fh:
                    content = pickle.load(fh)
                print(f"Address book loaded successfully from '{full_file_path}'.")
                return content
            else:
                print(f"File '{full_file_path}' not found. Creating a new address book.")
                return {}
        else:
            print("File not specified. Unable to load the address book.")
            return {}

    def search(self, query):
        result = []
        for el in self.data.values():
            if found_user := el.find_user_by_phone_name(query):
                result.append(found_user)
        return result
