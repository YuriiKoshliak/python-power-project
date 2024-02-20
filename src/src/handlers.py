from src.classes import AddressBook, Record, Notes, BodyOfNote, TegNote
from src.cleaner import sorting
import pickle
import re
from pathlib import Path


NOTEBOOK = AddressBook()
FILE_NAME = 'data.bin'
NOTES = Notes()
main_folder_path = None
contacts = {}
phone_pattern = r'\d+'
name_pattern = r'[a-zA-Z_]+'
operator_pattern = r'(edit note)|(add note)|(delete note)|(delete phone)|(show all)|(good bye)|[a-zA-Z_]+\s?'
phone_operator_pattern = r'(add)|(change)|(delete phone)'

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

# function to trim operator and name for email, adddress, birthday
def operator_trimmer(pattern: str, operator):
    trimmed = re.sub(pattern, '', operator)
    phoneName = re.search(name_pattern, trimmed).group().capitalize()
    userData = re.sub(phoneName, '', trimmed).strip() if re.search(phoneName, trimmed) \
        else re.sub(phoneName.casefold(), '', trimmed).strip()
    
    return [phoneName, userData]

#Simple welcome function
def hello(operator):
    return 'How can I help you?'

# Adds a phone number to the contacts list
def add_contact(operator):
    phoneName = operand_maker(operator)[0]
    phoneNum = operand_maker(operator)[1]

    record = NOTEBOOK.find(phoneName)
    try:
        if record != None:
            record.add_phone(phoneNum[0])

            return f'Phone to contact {phoneName} has been added!'   
        else:
            new_record = Record(phoneName)
            new_record.add_phone(phoneNum[0])

            NOTEBOOK.add_record(new_record)

            return f'Contact {phoneName} has been added!' 
    except ValueError:
        return "Wrong phone number format!"

# Adds a birthday to the contacts
def add_birthday(operator):
    contactData = operator_trimmer('birthday', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        record.add_birthday(contactData[1])

        return f'Contact {contactData[0]} has a birthday now!'   
    else:
        return f'Woopsie no contact with {contactData[0]} name!' 

# Adds the address to the contacts
def add_address(operator):
    contactData = operator_trimmer('address', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        record.add_address(contactData[1])

        return f'Contact {contactData[0]} has a address {contactData[1]} now!'   
    else:
        return f'Woopsie no contact with {contactData[0]} name!'

# Adds the email to the contacts
def add_email(operator):
    contactData = operator_trimmer('email', operator)

    record = NOTEBOOK.find(contactData[0])
    if record != None:
        record.email = contactData[1]

        return f'Contact {contactData[0]} has a address {contactData[1]} now!'   
    else:
        return f'Woopsie no contact with {contactData[0]} name!'

# Adds note
def add_note(operator):
    trimmed = re.sub('add note', '', operator).strip()

    if len(trimmed) >= 1:
        NOTEBOOK.write_note(trimmed)

        return 'Note added!'
    else:
        return "You should've write something!"

# Adds tag to the note with specified ID
def add_tag(operator):
    trimmed = re.sub('tag', '', operator).strip()
    index = re.search(r'[0-9]+', trimmed).group()
    teg = re.sub(index, '', trimmed).strip()

    NOTEBOOK.add_teg_to_note(index, teg)
    return f'Note {index} has teg: {teg}.'

# Finds note with specified ID/Tag/Word
def find_note(operator):
    trimmed = re.sub('note', '', operator).strip()
    note = NOTEBOOK.search_of_note(trimmed)

    return note

# Edits note with specified ID
def edit_note(operator):
    trimmed = re.sub('edit note', '', operator).strip()
    index = re.search(r'[0-9]+', trimmed).group()
    new_text = re.sub(index, '', trimmed).strip()

    NOTEBOOK.change_note(index, new_text)

    return f'Note {index} was updated!'

# Deletes note with specified ID
def delete_note(operator):
    trimmed = re.sub('delete note', '', operator).strip()
    
    try:
        NOTEBOOK.delete_the_note(trimmed)
        return f'Note {trimmed} was deleted!'
    except KeyError:
        return f'No note with that key!'

# This function isn't working so far
def sort_notes(operator): 
    # notes = NOTEBOOK.sorting_of_notes()
    ...
    # return notes

# Shows all notes
def show_notes(operator):
    notes = NOTEBOOK.show_all_notes()

    return f'{notes}'

# Shows birthdays within certain time range
def show_birthdays(operator):
    trimmed = re.sub('birthdays', '', operator).strip()

    return NOTEBOOK.list_with_birthdays(int(trimmed))

# Update the contact number
def change(operator):
    phoneName = operand_maker(operator)[0]
    phoneNums = operand_maker(operator)[1]

    contact = NOTEBOOK.find(phoneName)
    try:
        contact.edit_phone(phoneNums[0], phoneNums[1])

        return f'Contact {phoneName} has been updated!'
    except ValueError:
        return "Wrong phone number format or no such number!"

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

# Launch cleaner
def launch_cleaner(operator):
    global main_folder_path
    main_folder_path = Path(input('Enter the path for sorting and cleaning: '))
    sorting()

# Simple farewell function
def goodbye(operator):
    save_notebook(operator)
    return 'Your data is saved! Good bye!'

# Saving a notebook
def save_notebook(operator):
    try:
        with open (FILE_NAME, "wb") as file:
            pickle.dump(NOTEBOOK.data, file)
        
        return "Data was saved to file!"
    except IOError as E:
        print(E)

# Loadind a notebook
def load_notebook(operator):
    try:
        with open (FILE_NAME, "rb") as file:
            NOTEBOOK.data = pickle.load(file)
        return "Data was loaded from file!"
    except IOError as E:
        print(E)

# Shows commad list
def commands(operator):
    return 'The list of commands: \n \
        Type "contact [name of the contact]" to see its phone num.\n \
        Type "phone [phone of the contact]" to see if its exist.\n \
        Type "add [name] [phone number]" to add new contact.\n \
        Type "change [name] [old phone number] [new phone number]" to change phone number.\n \
        Type "birthday [name] [birthday date in date format]" to add bDay to the contact.\n \
        Type "email [name] [email]" to add email to the contact.\n \
        Type "delete phone [name] [phone number]" to delete phone from the contact.\n \
        Type "delete [name]" to delte the contact.\n \
        Type "birthdays [period of time in days]" to show the contacts with birthdays within this periond.\n \
        Type "show all" to see all contacts. \n \
            <-------------------------------->\n \
        To save data as file or work with saved book use next commands: \n \
            \n \
        Type "save" to save the address book (rewrite old book!!!) \n \
        Type "load" to open saved file. \n \
            <-------------------------------->\n \
        To work with notes use next commands: \n \
            \n \
        Type "add note [text]" to add new note.\n \
        Type "change [name] [old phone number] [new phone number]" to add new contact.\n \
        Type "note [id/tag/word] find note.\n \
        Type "tag [id] to add tag.\n \
        Type "delete note [id] to delete note.\n \
        Type "notes" to see all notes.\n \
            <-------------------------------->\n \
        To launch cleaner type "clean" \n \
            <-------------------------------->\n \
        And the ultimate command: \n \
            \n \
        Type "end" to exit'

OPERATIONS = {
    'hello': hello,
    'add': add_contact,
    'change': change,
    'delete phone': delete_phone,
    'delete': delete,
    'contact': contact,
    'show all': show_all,
    'add note': add_note,
    'note': find_note,
    'delete note': delete_note,
    'edit note': edit_note,
    'notes': show_notes,
    'tag': add_tag,
    'goodbye': goodbye,
    'birthday': add_birthday,
    'birthdays': show_birthdays,
    'address': add_address,
    'save': save_notebook,
    'email': add_email,
    'load': load_notebook,
    'clean': launch_cleaner,
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