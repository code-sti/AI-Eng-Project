# Learning Guide: Contact Book (CRUD, JSON Storage)

This file walks through exactly how this project was built, step by step, with every concept explained. Build it yourself using the steps below before looking at the final code.

**Prerequisite:** Project 2 (To-Do List App) — this project reuses its file/JSON storage pattern and adds new concepts on top.

---

## Goal

Build a command-line contact book with full CRUD (Create, Read, Update, Delete) on richer, multi-field records, plus search — all persisted to a JSON file.

---

## Step 1 — Load and save contacts (reusing a known pattern)

```python
import json
import os

FILENAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(FILENAME, "w") as file:
        json.dump(contacts, file, indent=4)
```

**What's happening:** Identical logic to the to-do list's `load_tasks()`/`save_tasks()`, just renamed for contacts.

**Why it matters:** Recognizing that you've already solved this exact shape of problem before — and reusing the pattern instead of reinventing it — is a real engineering instinct. Most "new" problems are actually old problems wearing different clothes.

---

## Step 2 — Add a contact (richer data model)

```python
def add_contact(contacts):
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print(f"Added contact: {name}")
```

**What's happening:** Each contact is a dictionary with **three** fields instead of the to-do list's two.

**Why it matters:** This is a **data modeling** decision — deciding what fields a record needs. This exact decision (what fields does a "thing" need?) is something you'll make constantly: database schemas, API request bodies, and later, Pydantic models all start with this same question.

---

## Step 3 — View all contacts

```python
def view_contacts(contacts):
    if not contacts:
        print("No contacts yet.")
        return
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact['name']} | {contact['phone']} | {contact['email']}")
```

**What's happening:** Same `enumerate()` pattern as the to-do list, now printing three fields per record instead of one.

---

## Step 4 — Search for a contact (new concept: list comprehensions)

```python
def search_contact(contacts):
    query = input("Enter name to search: ").lower()
    results = [c for c in contacts if query in c["name"].lower()]
    if not results:
        print("No matches found.")
        return
    for contact in results:
        print(f"{contact['name']} | {contact['phone']} | {contact['email']}")
```

**What's happening:** `[c for c in contacts if query in c["name"].lower()]` is a **list comprehension** — it builds a new list containing only the contacts whose name includes the search term. Read it as: *"give me each contact `c` from `contacts`, but only keep it if `query` appears in that contact's lowercased name."*

**Why it matters:** List comprehensions are one of the most common Python patterns you'll see from here on — a compact replacement for writing a manual loop with an `if` and `.append()`. `.lower()` on both sides makes the search case-insensitive, so searching "jo" matches "John" or "JOHN" equally.

---

## Step 5 — Update a contact (new concept: partial updates)

```python
def update_contact(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        num = int(input("Enter contact number to update: "))
        contact = contacts[num - 1]
        print("Leave blank to keep current value.")
        new_name = input(f"Name ({contact['name']}): ")
        new_phone = input(f"Phone ({contact['phone']}): ")
        new_email = input(f"Email ({contact['email']}): ")

        if new_name:
            contact["name"] = new_name
        if new_phone:
            contact["phone"] = new_phone
        if new_email:
            contact["email"] = new_email

        save_contacts(contacts)
        print("Contact updated.")
    except (ValueError, IndexError):
        print("Error: Invalid contact number.")
```

**What's happening:** We fetch the existing contact into a variable, show its current values as a hint in each prompt, and only overwrite a field **if the user actually typed something**. `if new_name:` works because an empty string (what you get from pressing Enter with nothing typed) is treated as `False` in Python.

**Why it matters:** This is the genuinely new concept in this project, and it's the missing piece from the to-do list's CRUD (which only had Create, Read, Delete — no Update). Real-world update forms almost never require re-entering every field just to change one — this "partial update" pattern is how that actually works under the hood.

---

## Step 6 — Delete a contact

```python
def delete_contact(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        num = int(input("Enter contact number to delete: "))
        removed = contacts.pop(num - 1)
        save_contacts(contacts)
        print(f"Deleted: {removed['name']}")
    except (ValueError, IndexError):
        print("Error: Invalid contact number.")
```

**What's happening:** Identical structure to the to-do list's delete function — same `try/except (ValueError, IndexError)` and `.pop()` pattern.

**Why it matters:** Notice how fast this was to write, having already built the same pattern once before. This is what "fluency" actually feels like — patterns become automatic instead of something you have to think through each time.

---

## Step 7 — Main menu

```python
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
            add_contact(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

main()
```

**What's happening:** Same `while True` + `break` loop pattern as the to-do list, with one extra menu option for search/update.

---

## Topics Covered

| Topic | Where it's used |
|---|---|
| File I/O + JSON persistence (review) | Steps 1 |
| Richer data models (multi-field dictionaries) | Step 2 |
| List comprehensions | Step 4 |
| Case-insensitive string matching | Step 4 |
| Partial updates (conditional field overwrite) | Step 5 |
| Truthy/falsy values in Python (`if new_name:`) | Step 5 |
| Multiple exception types in one block (review) | Steps 5 & 6 |

---

## Soft Skills Built

**Recognizing and reusing patterns.** Steps 1, 3, and 6 were nearly identical to the to-do list project — noticing this and reusing the pattern instead of rewriting from scratch is exactly how experienced engineers move faster over time without cutting corners.

**Designing for the real user experience.** The partial-update logic (Step 5) exists because forcing a user to re-type everything just to fix one typo is bad design. Thinking about *how someone will actually use* what you build — not just whether it technically works — is a skill that matters just as much in client-facing solutioning later as it does here.

---

## Test It Yourself

1. Add 2–3 contacts
2. Search a partial name (e.g., "jo" for "John") — confirm it matches
3. Update just the phone number on one contact, leaving name/email blank — confirm only the phone changed
4. Delete one contact — confirm it's removed
5. Close and reopen the program — confirm everything persisted

---

## Suggested Extra-Skill Upgrade (Resume Booster)

Once this version works, try rebuilding the contact data model using **Pydantic** instead of plain dictionaries. Define a `Contact` class with typed fields (and even basic email format validation), and use it in place of the raw dictionary.

This matters more than it looks: Pydantic is exactly what you'll use later for **FastAPI request validation** (Stage 2) and **structured outputs from LLMs / tool calling** (Stage 3–4). Learning it now, on a project you already understand, makes those later stages significantly easier.

**Free resources:**
- Official Pydantic docs: https://docs.pydantic.dev/latest/
- Official GitHub repo (see the `docs/examples` folder for real usage): https://github.com/pydantic/pydantic

## What's Next

**Project F.4: Number-Guessing Game** — introduces loops driven by a win/lose condition and basic randomness (the `random` module).