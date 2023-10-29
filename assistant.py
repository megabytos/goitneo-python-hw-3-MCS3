from contacts import AddressBook, Record, errors_handler
import pickle


def write_contacts_to_file(filename, contacts):
    with open(filename, "wb") as fh:
        pickle.dump(contacts, fh)


def read_contacts_from_file(filename):
    with open(filename, "rb") as fh:
        return pickle.load(fh)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@errors_handler
def add_contact(args, book):
    name, phone = args
    if book.record_exist(name):
        record = book.find(name)
        record.add_phone(phone)
        print("Phone added.")
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print("Contact added.")


@errors_handler
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    print("Contact updated.")


@errors_handler
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    print("Contact deleted.")


@errors_handler
def show_phone(args, book):
    name = args[0]
    print(book.find(name))


@errors_handler
def show_all(book):
    book.show_all()


@errors_handler
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    record.add_birthday(bday)
    print("Birthday added.")


@errors_handler
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    record.show_birthday()


@errors_handler
def birthdays(book):
    book.get_birthdays_per_week()


def main():
    try:
        book = read_contacts_from_file("contacts.bin")
        if not isinstance(book, AddressBook):
            book = AddressBook()
    except FileNotFoundError:
        book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            write_contacts_to_file("contacts.bin", book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            add_contact(args, book)
        elif command == "change":
            change_contact(args, book)
        elif command == "del":
            delete_contact(args, book)
        elif command == "phone":
            show_phone(args, book)
        elif command == "add-birthday":
            add_birthday(args, book)
        elif command == "show-birthday":
            show_birthday(args, book)
        elif command == "birthdays":
            birthdays(book)
        elif command == "all":
            show_all(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
