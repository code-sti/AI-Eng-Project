# Learning Guide: To-Do List App (File-Based Storage)

This file walks through exactly how this project was built, step by step, with every concept explained. If you're following this as part of the Zero-to-Senior AI Engineer + Solutions Architect path, build this project yourself using the steps below before looking at the final code.

**Prerequisite:** Project 1 (CLI Calculator) — this project assumes you're comfortable with `input()`, `try`/`except`, and `if`/`elif`/`else`.

---

## Goal

Build a command-line to-do list that lets you add, view, complete, and delete tasks — and remembers everything even after you close and reopen the program.

---

## Step 1 — Load tasks from a file when the program starts

```python
import json
import os

FILENAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []
```

**What's happening:** We're storing tasks in a JSON file. `os.path.exists(FILENAME)` checks whether that file already exists — the first time you ever run the app, it won't, so we return an empty list `[]` instead of crashing trying to open a missing file. `with open(...)` opens the file safely and closes it automatically when done. `json.load(file)` reads the JSON content and converts it into a Python list.

**Why it matters:** This is the first time in the series that a program needs to check "has this run before?" — a pattern you'll see constantly in real applications (databases, config files, caches).

---

## Step 2 — Save tasks back to the file

```python
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)
```

**What's happening:** `"w"` mode means "write," which overwrites the file with the current state of `tasks`. `json.dump()` converts the Python list into JSON text and writes it to disk. `indent=4` just makes the file human-readable if you open it manually.

**Why it matters:** We'll call this function after *every* change (add, complete, delete) — this is the core idea of **persistent state**: the file on disk should always match what's currently true in the program.

---

## Step 3 — Add a task

```python
def add_task(tasks):
    title = input("Enter task: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")
```

**What's happening:** Each task is a **dictionary** with two fields: `title` and `done`. `tasks.append(...)` adds it to the in-memory list, then we immediately call `save_tasks()` so the change is written to disk right away.

**Why it matters:** This introduces a **data model** — deciding what shape your data takes (here, a dictionary with two fields) is a decision you'll make constantly in software engineering, and it directly affects how easy or hard everything downstream becomes.

---

## Step 4 — View all tasks

```python
def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        print(f"{index}. [{status}] {task['title']}")
```

**What's happening:** `enumerate(tasks, start=1)` loops through the list and gives you both a position number (starting at 1, so it reads naturally to a human) and the item itself. `task["done"]` reads the dictionary's `done` field, and a one-line `if/else` picks a checkmark or blank space.

**Why it matters:** This function only *displays* data — it never modifies it, so it never calls `save_tasks()`. Separating "read" operations from "write" operations is a habit that becomes very important later (it's the same principle behind database read/write separation).

---

## Step 5 — Mark a task as done

```python
def complete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to mark done: "))
        tasks[num - 1]["done"] = True
        save_tasks(tasks)
        print("Marked as done.")
    except (ValueError, IndexError):
        print("Error: Invalid task number.")
```

**What's happening:** We show the list first so the user knows what number to choose. `tasks[num - 1]` — since the display starts counting at 1 but Python lists are indexed from 0, we subtract 1 to find the right item.

**Why it matters:** The `try/except` here catches **two different error types in one line**: `ValueError` (user typed non-numeric text) and `IndexError` (user typed a number that doesn't exist in the list, like `99` when there are only 3 tasks). Grouping exception types in a tuple `(ValueError, IndexError)` is a clean way to handle multiple failure modes with one message, when the user-facing response is the same either way.

---

## Step 6 — Delete a task

```python
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to delete: "))
        removed = tasks.pop(num - 1)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}")
    except (ValueError, IndexError):
        print("Error: Invalid task number.")
```

**What's happening:** `tasks.pop(num - 1)` removes the item at that position **and returns it**, which is why we can print exactly what was deleted.

**Why it matters:** Notice this function is almost identical in structure to `complete_task` — same error handling, same flow. Recognizing repeated patterns like this is what eventually leads to writing more reusable, DRY (Don't Repeat Yourself) code.

---

## Step 7 — The main menu loop

```python
def main():
    tasks = load_tasks()
    while True:
        print("\n--- To-Do List ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task done")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

main()
```

**What's happening:** `tasks = load_tasks()` runs once at the very start, restoring any previously saved tasks. `while True:` creates an infinite loop so the menu keeps reappearing. Each choice routes to one of the functions we already built. `break` is what actually exits the loop when the user chooses "5" — without it, "Goodbye!" would print but the menu would immediately reappear anyway.

**Why it matters:** This is why we built everything above as separate, small functions instead of one giant block of code — the main loop stays short and readable because it just *routes* to functions rather than containing all the logic itself.

---

## Topics Covered

| Topic | Where it's used |
|---|---|
| File I/O (`open`, `with`, read/write modes) | Steps 1 & 2 |
| JSON serialization (`json.load`, `json.dump`) | Steps 1 & 2 |
| Persistent state across program runs | Steps 1 & 2 |
| Dictionaries as a data model | Step 3 |
| `enumerate()` for indexed loops | Step 4 |
| Multiple exception types in one `except` block | Steps 5 & 6 |
| List indexing and `.pop()` | Step 6 |
| `while True` loops with `break` | Step 7 |
| Structuring code into small, single-purpose functions | Throughout |

---

## Soft Skills Built

**Breaking a problem into small pieces.** Instead of one giant script, this project is split into 7 functions, each doing exactly one job. This decomposition instinct is the foundation of good system design — the same thing you'll do later when architecting multi-agent systems or enterprise solutions, just at a larger scale.

**Thinking about the full lifecycle of data**, not just the moment it's created — where does it live, how does it get saved, what happens when the program restarts? This "full lifecycle" mindset is exactly what shows up later when designing databases, agent memory, or knowledge graphs.

---

## Test It Yourself

1. Add 2–3 tasks
2. View the list — confirm they appear
3. Mark one as done — confirm the checkmark shows
4. **Close the program completely and reopen it** — confirm your tasks are still there (this proves file persistence works)
5. Try entering `99` when completing/deleting — confirm you get a clean error, not a crash
6. Delete a task — confirm it's removed from the list

## What's Next

**Project 3: Contact Book (CRUD, JSON storage)** — builds directly on this project's file/JSON pattern, adding full Create/Read/Update/Delete operations on richer data (multiple fields per contact).