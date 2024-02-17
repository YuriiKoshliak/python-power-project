from classes import AddressBook, Record, Birthday, Phone, Name
import pickle

# creating a notebook
NOTEBOOK = AddressBook()
FILE_NAME = 'data.bin'

# saving a notebook
def save_notebook():
    try:
        with open (FILE_NAME, "wb") as file:
            pickle.dump(NOTEBOOK.data, file)
    except IOError as E:
        print(E)

# loadind a notebook
def load_notebook():
    try:
        with open (FILE_NAME, "rb") as file:
            NOTEBOOK.data = pickle.load(file)
        print("Data was loaded from save")
    except IOError as E:
        print(E)




if __name__ == '__main__':
    ...