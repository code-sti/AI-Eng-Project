import json
import os

FILENAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILENAME):
        with open (FILENAME,"r") as file:
            return json.load(file)
    return []
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks):
    title = input("Enter task: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")
def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    for index , task in enumerate(tasks):
        status = "✓" if task["done"] else " "
        print(f"{index} . [{status}] {task['title']}")
def complete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to mark done: "))
        tasks[num-1]["done"] = True
        save_tasks(tasks)
        print("Marked as done.")
    except(ValueError, IndexError):
        print("Error: Invalid task number.")
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to mark done: "))
        removed = tasks.pop(num-1)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}")
    except(ValueError, IndexError):
        print("Error: Invalid task number.")
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
