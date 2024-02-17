from classes import AddressBook, Record, Birthday, Phone, Name
import handlers

waiting = True
goodbyes = ("good bye", "close", "exit", "end", "bye")
# creating a notebook
# NOTEBOOK = AddressBook()
# FILE_NAME = 'data.bin'

# request-response cycle
def main_action(func):
    def inner(operator):
        try:
            func(operator)
        except AttributeError:
            print('Check twice or type the "commands" to print the list of commands!')
        except Exception as e:
            message = str(e)
            print(message)
    
    return inner

@main_action
def main(operator) -> str:
    # handler = handlers.get_handler(operator)
    handler = handlers.get_handler(operator)

    print(handler(operator))


if __name__ == '__main__':
    while waiting == True:
        operator = input(":")
        if operator in goodbyes:
            main('goodbye')
            break 
        else: 
            main(operator)