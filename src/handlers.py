from classes import AddressBook, Record, Address, Birthday, Phone, Name
import pickle
import re
# import classes


contacts = {}
phone_pattern = r'\d+'
name_pattern = r'[a-zA-Z_]+'
operator_pattern = r'(delete phone)|(show all)|(good bye)|[a-zA-Z_]+\s?'
phone_operator_pattern = r'(add)|(change)|(delete phone)'
NOTEBOOK = AddressBook()
FILE_NAME = 'data.bin'


# Remove spaces at the beginning and at the end of the string and lower case the string
def operator_handler(operator):
    parced_operator = re.search(operator_pattern, operator)
    return parced_operator.group().lower().strip()

# Defines name and telephone number
def operand_maker(operator):
    operands = []
    trimmedContact = re.sub(phone_operator_pattern, '', operator)
    
    phoneName = re.search(name_pattern, trimmedContact)
    phoneNums = re.findall(phone_pattern, trimmedContact)
    
    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneName.group().capitalize())
    
    if not phoneNums:
        raise Exception('No number? Enter the contact in the format: "Name" "Phone Number"')
    else:
        operands.append(phoneNums)

    return operands

#Simple welcome function
def hello(operator):
    return 'How can I help you?'

# Adds a phone number to the contacts list
def add(operator):
    phoneName = operand_maker(operator)[0]
    phoneNum = operand_maker(operator)[1]

    record = NOTEBOOK.find(phoneName)
    if record != None:
        record.add_phone(phoneNum[0])

        return f'Phone to contact {phoneName} has been added!'   
    else:
        new_record = Record(phoneName)
        new_record.add_phone(phoneNum[0])

        NOTEBOOK.add_record(new_record)

        return f'Contact {phoneName} has been added!' 

# Adds a birthday to the contacts
def birthday(operator):
    trimmed = re.sub('birthday', '', operator)
    phoneName = re.search(name_pattern, trimmed).group().capitalize()
    bDay = re.sub(phoneName, '', trimmed).strip()

    record = NOTEBOOK.find(phoneName)
    if record != None:
        record.add_birthday(bDay)

        return f'Contact {phoneName} has a birthday now!'   
    else:
        return f'Woopsie no contact with {phoneName} name!' 

def address(operator):
    trimmed = re.sub('address', '', operator)
    phoneName = re.search(name_pattern, trimmed).group().capitalize()
    addressData = re.sub(phoneName, '', trimmed).strip()

    record = NOTEBOOK.find(phoneName)
    if record != None:
        record.add_address(addressData)

        return f'Contact {phoneName} has a address now!'   
    else:
        return f'Woopsie no contact with {phoneName} name!'

def email(operator):
    ...

# Update the contact number
def change(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = NOTEBOOK.find(phoneName)
    contact.edit_phone(phoneNums[0], phoneNums[1])

    return f'Contact {phoneName} has been updated!'

# Delete the contact number for a certain contact
def delete_phone(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = NOTEBOOK.find(phoneName)
    contact.remove_phone(phoneNums[0])

    return f'Phone {phoneNums[0]} was deleted fron contact {phoneName}!'

# Delete the contact
def delete(operator):
    phoneName = re.search(name_pattern, operator.replace("delete", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    
    capitalized_name = phoneName.group().capitalize()
    NOTEBOOK.delete(capitalized_name)

    return f'Contact {capitalized_name} was deleted!'

# Displays the phone number of the requested contact
def contact(operator):
    phoneName = re.search(name_pattern, operator.replace("contact", ""))

    if not phoneName:
        raise Exception('No name? Enter the contact in the format: "Name" "Phone Number"')
    
    capitalized_name = phoneName.group().capitalize()
    record = NOTEBOOK.find(capitalized_name)

    return record

# Shows contact list
def show_all(operator):
    book_view = NOTEBOOK.custom_iterator(len(NOTEBOOK))
    return f'{next(book_view)}'

# Simple farewell function
def goodbye(operator):
    save_notebook(operator)
    return 'Good bye!'

# saving a notebook
def save_notebook(operator):
    try:
        print('inside the save function')
        with open (FILE_NAME, "wb") as file:
            pickle.dump(NOTEBOOK.data, file)
            
    except IOError as E:
        print(E)

# loadind a notebook
def load_notebook(operator):
    try:
        with open (FILE_NAME, "rb") as file:
            NOTEBOOK.data = pickle.load(file)
        print("Data was loaded from save")
    except IOError as E:
        print(E)

# Shows commad list
def commands(operator):
    return 'The list of commands: \n \
        Type "contact [name of the contact]" to see its phone num.\n \
        Type "phone [phone of the contact]" to see if its exist.\n \
        Type "add [name] [phone number]" to add new contact.\n \
        Type "change [name] [old phone number] [new phone number]" to add new contact.\n \
        Type "birthday [name] [birthday date in date format]" to add bDay to the contact.\n \
        Type "delete phone [name] [phone number]" to delete phone from the contact.\n \
        Type "delete [name]" to delte the contact.\n \
        Type "show all" to see all contacts \n \
        To sava data as file or work with saved book use next commands: \n \
        Type "save" to save the address book (rewrite old book!!!) \n \
        Type "load" to open saved file \n \
        And the ultimate command: \n \
        Type "end" to exit'

OPERATIONS = {
    'hello': hello,
    'add': add,
    'change': change,
    'delete phone': delete_phone,
    'delete': delete,
    'contact': contact,
    'show all': show_all,
    'goodbye': goodbye,
    'birthday': birthday,
    'address': address,
    'save': save_notebook,
    'load': load_notebook,
    'help': commands
}

def get_handler(operator):
    operator = operator_handler(operator)
    if operator not in OPERATIONS:
        raise AttributeError
    else:
        return OPERATIONS[operator]

if __name__ == '__main__':
    print('Go to the main file!')