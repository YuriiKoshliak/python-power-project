from address_book import AddressBook
from record import Record
from field import Field

def input_error(func):
    def wrapper(command):
        try:
            return func(command)
        except (TypeError) as e:
            return f"Input error of type: {e}"
        except (IndexError) as e:
            return f"Input error: {e}"
        except (ValueError) as e:
            return f"Input 3 arguments only(example: command name phone): {e}"
        except (KeyError) as e:
            return f"Input error: {e}"
        except Exception as e:
            return "Command error"

    return wrapper

@input_error
def add(command):
    com, name, phone, email = command.split()
    if com != "add":
        raise Exception("Incorrect command name, try again")
    if name in book.data:
        raise KeyError("This name is exist")

    new_record = Record(name, email)
    new_record.add_phone(phone)
    book.add_record(new_record)
    book.save_address_book()  # Збереження адресної книги при додаванні нового запису
    return "Record added successfully."

@input_error
def change(command):
    com, name, phone = command.split()
    if com != "change":
        raise Exception("Incorrect command name, try again")
    if name not in book.data:
        raise KeyError("This name is not exist")

    record = book.find(name)
    record.edit_phone(record.phones[0].value, phone)
    book.save_address_book()  # Збереження адресної книги при зміні номера телефону
    return "Phone number changed successfully."

@input_error
def phone(command):
    com, name = command.split()
    if com != "phone":
        raise Exception("Incorrect command name, try again")
    if name not in book.data:
        raise KeyError("This name is not exist")

    record = book.find(name)
    return f"{record.name.value} has phone {record.phones[0].value}"

def show_all(com):
    if com != "show all":
        raise Exception("Incorrect command name, try again")
    result = [str(record) for record in book.data.values()]
    return "\n".join(result)

def search(query):
    results = book.search(query)
    if results:
        print("Search Results:")
        for result in results:
            print(result)
    else:
        print("No matching records found.")

COMMANDS = {
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "search": search,
}

@input_error
def command_action(command):
    for el in COMMANDS:
        if command.startswith(el):
            return COMMANDS[el]
    raise Exception("Incorrect command name, try again")

book = AddressBook(file="example.pkl")
book.data = book.load_address_book()

def main():
    print("Welcome to the Address Book Program!")
    print("Available commands:")
    print("1. add <name> <phone> <email> - Add a new record to the address book.")
    print("2. change <name> <phone> - Change the phone number of an existing record.")
    print("3. phone <name> - Retrieve the phone number for a specific name.")
    print("4. show all - Display all records in the address book.")
    print("5. search <query> - Search for records based on a query.")
    print("6. hello - Display a welcome message.")
    print("7. good bye, close, exit, . - Exit the program.")

    while True:
        print()
        command = input("Enter your command: ").lower()
        if command in ["good bye", "close", "exit", "."]:
            # Save the address book before exiting the program
            book.save_address_book()
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
            continue
        else:
            func = command_action(command)
            if func == "Command error":
                print(func)
                continue
            result = func(command)
            if result == "break":
                break
            elif result:
                print(result)

if __name__ == "__main__":
    main()