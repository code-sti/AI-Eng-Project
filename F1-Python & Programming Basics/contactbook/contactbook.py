import json
import os

FILENAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    return []

def save_contacts(contacts):
    with open(FILENAME,'w') as file:
        json.dump(contacts, file, indent=4)

def add_contacts(contacts):
    name = input("name:")
    email = input("email:")
    phone = input("phone:")
    contacts.append({"name": name, "phone": phone, "email":email })
    save_contacts(contacts)
    print(f"Added contact: {name}")

def view_contacts(contacts):
    if not contacts:
        print("No contacts")
        return
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact['name']} | {contact['email']} | {contact['phone']}")

def search_contacts(contacts):
    query = input("Enter name to search: ").lower()
    results = [c for c in contacts if query in c['name'].lower()]
    if not results:
        print("No matches found.")
        return
    for contact in results:
        print(f"{contact['name']} | {contact['email']} | {contact['phone']}")

def update_contact(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        num = int(input("Enter contact number to update: "))
        contact = contacts[num - 1]
        print("leave blank to keep current value. ")
        new_name = input(f"Name ({contact['name']}): ")
        new_phone = input(f"Phone ({contact['phone']}): ")
        new_email = input(f"Email ({contact['email']}): ")

        if new_name:
            contact["name"] = new_name

        if new_email:
            contact["email"] = new_email

        if new_phone:
            contact["phone"] = new_phone
        save_contacts(contacts)
        print("Contact Saved")
    except(ValueError, IndexError):
        print("Error: Invalid contact number.")

def delete_contacts(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        num = int(input("Enter Contact number to delete"))
        removed = contacts.pop(num-1)
        save_contacts(contacts)
        print(f"Deleted:{removed['name']}")
    except (ValueError, IndexError):
        print("Error: Invalid contact number.")

def main():
    contacts = load_contacts()
    while True:
        print("\n--- Contact Book ---")
        print("1. View contacts")
        print("2. Add contact")
        print("3. Search contact")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_contacts(contacts)
        elif choice == "2":
            add_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contacts(contacts)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

main()