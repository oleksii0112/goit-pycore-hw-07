from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self,value):
        if not value.isdigit() or len(value) !=10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_obj)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)
    
    def remove_phone(self,value):
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)
                break
                
    def edit_phone (self, old_value, new_value):
        for phone in self.phones:
            if phone.value == old_value:
                phone.value = Phone(new_value).value
    

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None     
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value.lower()] = record
    
    def find(self, name):
        return self.data.get(name.lower())
    
    def delete(self, name):
        key = name.lower()
        if key in self.data:
            del self.data[key]

    def birthdays(self):
        today= datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
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
    

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()