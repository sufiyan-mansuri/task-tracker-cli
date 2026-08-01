"""
Task Tracker CLI
=================
A simple command-line tool to add, update, delete, and track tasks.
Tasks are stored locally in a JSON file (tasks.json) in the current
working directory. No external libraries are used, only Python's
standard library (sys, os, json, datetime).

Project spec: https://roadmap.sh/projects/task-tracker

Usage:
    python main.py add "Buy groceries"
    python main.py update <id> "New description"
    python main.py delete <id>
    python main.py mark-in-progress <id>
    python main.py mark-done <id>
    python main.py list
    python main.py list done
    python main.py list todo
    python main.py list in-progress
"""

import os
import json
from datetime import datetime, timezone
import sys

TASKS_FILE = "tasks.json"

VALID_STATUSES = ("todo", "in-progress", "done")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: '{TASKS_FILE}' is corrupted or not valid JSON. Starting with an empty task list.")
        return []

    if not isinstance(data, list):
        print(f"Warning: '{TASKS_FILE}' is corrupted or not valid JSON. Starting with an empty task list.")
        return []

    return data

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def next_task_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def current_timestamp():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def cmd_add(args):
    if len(args) < 1:
        print("Error: please provide a task description.")
        print('Usage: python main.py add "<description>"')
        return

    description = args[0]
    tasks = load_tasks()

    task_id = next_task_id(tasks)
    timestamp = current_timestamp()

    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {task_id})")

def cmd_update(args):
    if len(args) < 2:
        print("Error: please provide a task ID and the new description.")
        print('Usage: python main.py update <id> "<new description>"')
        return

    task_id = parse_task_id(args[0])
    if task_id is None:
        return

    new_description = args[1]
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Error: no task found with ID {task_id}.")
        return

    task["description"] = new_description
    task["updatedAt"] = current_timestamp()
    save_tasks(tasks)

    print(f"Task {task_id} updated successfully.")

def cmd_delete(args):
    if len(args) < 1:
        print("Error: please provide a task ID.")
        print("Usage: python main.py delete <id>")
        return

    task_id = parse_task_id(args[0])
    if task_id is None:
        return

    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Error: no task found with ID {task_id}.")
        return

    tasks.remove(task)
    save_tasks(tasks)

    print(f"Task {task_id} deleted successfully.")

def cmd_mark(args, status):
    if len(args) < 1:
        print("Error: please provide a task ID.")
        print(f"Usage: python main.py mark-{status} <id>")
        return

    task_id = parse_task_id(args[0])
    if task_id is None:
        return

    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        print(f"Error: no task found with ID {task_id}.")
        return

    task["status"] = status
    task["updatedAt"] = current_timestamp()
    save_tasks(tasks)

    print(f"Task {task_id} marked as {status}.")

def cmd_list(args):
    status_filter = None

    if args:
        status_filter = args[0]
        if status_filter not in VALID_STATUSES:
            print(f"Error: '{status_filter}' is not a valid status.")
            print(f"Valid statuses are: {', '.join(VALID_STATUSES)}")

    tasks = load_tasks()

    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        if status_filter:
            print(f"No tasks with status '{status_filter}'.")
        else:
            print("No tasks found.")
        return

    for task in tasks:
        print(f"[{task['id']}] ({task['status']}) {task['description']}")
        print(f"      created: {task['createdAt']}  updated: {task['updatedAt']}")

def parse_task_id(raw_id):
    if not raw_id.isdigit():
        print(f"Error: task ID must be a positive number, got '{raw_id}'.")
        return None
    return int(raw_id)

def print_usage():
    print(__doc__)

COMMANDS = {
    "add": cmd_add,
    "update": cmd_update,
    "delete": cmd_delete,
    "list": cmd_list,
    "mark-in-progress": lambda args: cmd_mark(args, "in-progress"),
    "mark-done": lambda args: cmd_mark(args, "done"),
}

def main():
    argv = sys.argv[1:]  

    if not argv:
        print_usage()
        sys.exit(1)  

    command, rest = argv[0], argv[1:]    

    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Error: unknown command '{command}'.")
        print_usage()
        sys.exit(1)

    handler(rest)
    
if __name__ == "__main__":
    main()

        