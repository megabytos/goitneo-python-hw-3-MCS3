from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import re


class CustomExeption(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EmptyContacts(Exception):
    pass


class InvalidPhoneFormat(Exception):
    pass


class InvalidPhoneLegnth(Exception):
    pass


class InvalidDateFormat(Exception):
    pass


class ContactAlreadyExist(CustomExeption):
    pass


class PhoneAlreadyExist(CustomExeption):
    pass


class ContactNotFound(CustomExeption):
    pass


class PhoneNotFound(CustomExeption):
    pass


class BirthdayNotFound(Exception):
    pass


def errors_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid data."
        except KeyError:
            return "Item not found."
        except EmptyContacts:
            return "Contacts is empty."
        except InvalidPhoneLegnth:
            print("Invalid Phone Legnth, should be 10 digits")
        except InvalidPhoneFormat:
            print("Invalid Phone format, should be only digits")
        except PhoneAlreadyExist as arg:
            print(f'Phone "{arg.value}" already exist ')
        except PhoneNotFound as arg:
            print(f'Phone "{arg.value}" not Found ')
        except ContactNotFound as arg:
            print(f'Contact "{arg.value}" not Found ')
        except ContactAlreadyExist as arg:
            print(f'Contact "{arg.value}" already exist ')
        except InvalidDateFormat:
            print("Incorrect Date format, should be DD.MM.YYYY")
        except BirthdayNotFound:
            print("Birthday not found")

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise InvalidPhoneLegnth
        if not value.isdigit():
            raise InvalidPhoneFormat
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            raise InvalidDateFormat
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if self.find_phone(phone):
            raise PhoneAlreadyExist(phone)
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if not self.find_phone(phone):
            raise PhoneNotFound(phone)
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, phone, new_phone):
        if self.find_phone(new_phone):
            raise PhoneAlreadyExist(new_phone)
        if not self.find_phone(phone):
            raise PhoneNotFound(phone)
        for p in self.phones:
            if p.value == phone:
                idx = self.phones.index(p)
                self.phones[idx] = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if not self.birthday:
            raise BirthdayNotFound
        print(self.birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone
        return False

    def __str__(self):
        birthday = ", birthday: " + self.birthday.value if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        if name in self.data:
            raise ContactAlreadyExist(name)
        self.data[name] = record

    def find(self, name):
        if self.record_exist(name):
            return self.data.get(name)
        raise ContactNotFound(name)

    def record_exist(self, name):
        return name in self.data

    def delete(self, name):
        if name not in self.data:
            raise ContactNotFound(name)
        self.data.pop(name)

    def show_all(self):
        if not len(self.data):
            raise EmptyContacts
        print("\n".join(str(record) for record in self.data.values()))        

    def get_birthdays_per_week(self):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        week_birthdays = defaultdict(list, {i: [] for i in days_of_week})
        today = datetime.today().date()
        days_to_subtract = {0: 2, 6: 1}
        if today.weekday() in days_to_subtract:  # We must to take the previous weekend
            today = today - timedelta(days=days_to_subtract[today.weekday()])

        for user in self.data.values():
            name = user.name.value.title()
            if not user.birthday:
                continue
            birthday_obj = datetime.strptime(str(user.birthday), "%d.%m.%Y")
            birthday_date = birthday_obj.date()
            birthday = birthday_date.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            delta_days = (birthday - today).days
            if delta_days < 7:
                weekday_num = birthday.weekday()
                # If today is Sunday and birthday in next Saturday
                if weekday_num == 5 and delta_days == 6:
                    continue
                weekday = "Monday" if weekday_num in [5, 6] else birthday.strftime("%A")
                week_birthdays[weekday].append(name)

        for weekday, persons in week_birthdays.items():
            if persons:
                print(f'{weekday}: {", ".join(persons)}')
