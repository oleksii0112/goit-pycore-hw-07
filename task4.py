import re
from cli_bot import AddressBook, Record, Phone, Field
from datetime import datetime, timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            msg = str(e)
            if msg == "duplicate":
                return "This name is already used, change or add some symbols!"
            elif msg == "invalid add-birthday":
                return "Usage: add-birthday [name] [DD.MM.YYYY]"
            elif msg == "invalid show-birthday":
                return "Usage: show-birthday [name]"
            return "Invalid format! Usage: add [name] [phone]"
        except KeyError as e:
            name = e.args[0] if e.args else ""
            if name:
                return (f"There is no contact with name {name}.\nIf you want to add - type 'add [name] [number]'")
            return "This contact does not exist."
        except IndexError:
            return "The command format is 'add [name] [phone]'"
    return inner

def parse_input(user_input: str):
    inputs = user_input.strip().split()
    if not inputs:
        return "", []
    cmd, *args = inputs
    cmd = re.sub(r"[^a-z-]","",cmd.lower())
    return cmd, args

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if contacts.find(name):
        raise ValueError("duplicate")
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added"
    
@input_error    
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, new_phone = args
    record = contacts.find(name)
    if not record:
        raise KeyError(name)
    if record.phones:
        record.edit_phone(record.phones[0].value, new_phone)
    else:
        record.add_phone(new_phone)
    return f"Contact {record.name.value} updated"
    
def show_all(args, contacts):
    if not contacts:
        return "No contacts found."
    lines = []
    for record in sorted(contacts.data.values(), key=lambda r: r.name.value.lower()):
        phones = ', '.join(p.value for p in record.phones)
        lines.append(f"{record.name.value}: {phones}")
    return "\n".join(lines)

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = contacts.find(name)
    if not record:
        raise KeyError(name)
    phones = ', '.join(p.value for p in record.phones)
    return f"{record.name.value}`s number(s): {phones}"

@input_error
def add_birthday(args, book:AddressBook):
    if len(args) != 2:
        raise ValueError("invalid add-birthday")
    name, birthday_str = args
    record = book.find(name)
    if not record:
        raise KeyError(name)
    datetime.strptime(birthday_str, "%d.%m.%Y")
    record.add_birthday(birthday_str)
    return f"Birthday for {name} set to {birthday_str}"

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid show-birthday")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(name)
    if not record.birthday:
        return f"{name} does not have a birthday set."
    return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book: AddressBook):
        today= datetime.today().date()
        upcoming_birthdays = []

        for record in book.data.values():
            if not record.birthday:
                continue

            current_year_birthday = record.birthday.value.replace(year=today.year)

            if current_year_birthday < today:
                current_year_birthday = current_year_birthday.replace(year=today.year + 1)

            days_until_birthday = (current_year_birthday - today).days

            if 0 < days_until_birthday <= 7:
                if current_year_birthday.weekday() == 5:  # Saturday
                    current_year_birthday += timedelta(days=2)
                elif current_year_birthday.weekday() == 6:  # Sunday
                    current_year_birthday += timedelta(days=1)

                upcoming_birthdays.append(f"{record.name.value} -> {current_year_birthday.strftime('%d.%m.%Y')}")
 
        if not upcoming_birthdays:
            return "No birthdays in the next 7 days."
        return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)                                   


def main():
    contacts = AddressBook()
    print ("Welcome to the assistant bot! Type 'hello' to continue, 'exit/close' to exit")
    while True:
        user_input = input("Input a command: ")
        exit_cmd = ["exit", "close"]
        command, args = parse_input(user_input)
        if command in exit_cmd:
           print("Good bye!")
           break
        elif command == "hello":
            print("How can I help you? You can 'add', 'change' contacts,\nsee 'all' contacts, or 'phone' of specific contact,\n'add-birthday', 'show-birthday' or see all 'birthdays'  ")
        elif command == "add":
            print (add_contact(args, contacts))
        elif command == "change":
            print (change_contact(args, contacts))
        elif command == "all":
            print (show_all(args,contacts))
        elif command == "phone":
            print (show_phone(args, contacts ))
        elif command == "":
            continue
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")    

if __name__ == "__main__":
    main()