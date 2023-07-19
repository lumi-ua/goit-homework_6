from classes_hw6 import AddressBook, Name, Phone, Birthday, Record

address_book = AddressBook()
address_book_iterator = None


def input_error(func):
    def wrapper(*args):
        result = None
        try:
            result = func(*args) 
        except KeyError:
            print("Enter user name")
        except ValueError:
            print("Give me name and phone please")
        except IndexError:
            print("You entered incorrect data")
        except TypeError:
            print("Wrong input type")
        return result
    return wrapper     


@input_error
def hello(*args):
    return f"How can I help you?"

@input_error
def add(*args):
    name = args[0]
    number = args[1]
    address_book_iterator = None # грохаем итератор, т.к. после добавления новой записи он станет не валидный.
    if len(args) == 3:
        birthday = args[2]
        address_book.add_record(Record(Name(name), Phone(number), Birthday(birthday)))
        return f"Add success {name} {number} {birthday}"
    else:
        address_book.add_record(Record(Name(name), Phone(number)))
        return f"Add success {name} {number}"
    
@input_error
def change(*args):
    name = args[0]
    number_from = int(args[1])  #check if number, else generate exception
    number_to = int(args[2])    #check if number, else generate exception
    phone_from = args[1]
    phone_to = args[2]

    record = address_book.search_user(name)
    if record:
        record.change_phone(Phone(phone_from), Phone(phone_to))
        return f"Change success {name} {number_from}->{number_to}"
    return f"Change error {name} {number_from}->{number_to}"

@input_error
def phone(*args):
    name = args[0]
    record = address_book.search_user(name)
    if record:
        result = name + ": " + ", ".join([phone.value for phone in record.phone_list])
        if record.birthday:
            result += f"; {record.birthday.value.date()}" + "\ndays to birthday:" + str(record.days_to_birthday())
        return result
    return "ERROR empty"

@input_error
def show_all():
    return address_book

@input_error
def good_bye(*args):
    print("Good bye!")
    exit(0)
    return None

@input_error
def no_command(*args):
    return "Unknown command"

@input_error
def show_next(*args):
    global address_book_iterator
    if address_book_iterator:
        address_book_iterator = next(address_book_iterator)
    else:
        address_book_iterator = address_book.iterator()

    if address_book_iterator:
        return str(address_book_iterator)
    return None


COMMANDS = {
    hello: ("hello", "hi"),
    add: ("add", "+"),
    change: ("change", "edit"),
    phone: ("phone", "user"),
    show_all: ("show all", "all"),
    good_bye: ("exit", "close", "end"),
    show_next: ("next",)
}

def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
    return no_command, None

def main():
    while True:
        user_input = input(">>>")
        command, args = parser(user_input)
        if args != None:
            result = command(*args)
        else:
            result = command()
        
        if result: print(result)

###############################################
if __name__ == "__main__":
    main()
   