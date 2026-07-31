import sys
import datetime
import json
import os

args = sys.argv

if os.path.exists("tasks.json"):
    with open("tasks.json", "r") as file:
        try:
            tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []
else:
    tasks = []

if args[1] == "add":
    task_description_index = 2
    if 0 <= task_description_index < len(args):
        task_description = args[2]
        current_date_time = datetime.datetime.now()

        if len(tasks) > 0:
            task_id = len(tasks) + 1
        else:
            task_id = 1

        task_data = {
            'id': task_id,
            'description': task_description,
            'status': 'todo',
            'createdAt': current_date_time.strftime("%x %X"),
            'updatedAt': current_date_time.strftime("%x %X")
        }

        tasks.append(task_data)

        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)

        print("Task added succesfully.")
    else:
        print("Please add a description for your task.")

elif args[1] == "list":
    filter = None
    filter_count = 0 
    if "todo" in args or "in-progress" in args or "done" in args:
        filter = args[2]
    
    if tasks:
        print("=========== ALL TASKS ===========")
        for task in tasks:

            if filter and filter != task['status']:
                continue
            else:
                filter_count += 1

            print(f"ID             : {task['id']}")
            print(f"Description    : {task['description']}")
            print(f"Status         : {task['status']}")

        if filter_count <= 0:
            print("No tasks to show for this filter.")

        print("=================================")
    else:
        print("No tasks available.")

elif args[1] == "update":
    task_id_index = 2
    task_id_exists = 0 <= task_id_index < len(args)

    updated_task_description_index = 3
    updated_task_description_exists = 0 <= updated_task_description_index < len(args)

    if not task_id_exists:
        print("Task ID not given.")
    elif not updated_task_description_exists:
        print("Please enter the updated description.")
    else:
        task_id = args[task_id_index]
        if task_id.isdigit():
            updated_task_description = args[updated_task_description_index]
            current_date_time = datetime.datetime.now()

            for task in tasks:
                if task["id"] == int(task_id):
                    task["description"] = updated_task_description
                    task["updatedAt"] = current_date_time.strftime("%x %X")
                    break

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

            print("Task Updated Successfully.")
        else:
            print("Task ID can only be a number.")

elif args[1] == "delete":
    task_id_index = 2
    task_id_exists = 0 <= task_id_index < len(args)

    if not task_id_exists:
        print("Task ID not given.")
    else:
        task_id = args[task_id_index]

        if task_id.isdigit():
            task_index_to_remove = None

            if tasks:
                for index, task in enumerate(tasks, start=0):
                    if task["id"] == int(task_id):
                        task_index_to_remove = index
                        break

                tasks.pop(task_index_to_remove)

            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)

            print("Task deleted succesfully.")
        else:
            print("Task ID can only be a number.")

elif args[1] == "mark-in-progress" or args[1] == "mark-done":
    task_id_index = 2
    task_id_exists = 0 <= task_id_index < len(args)

    if not task_id_exists:
        print("Task ID not given.")
    else:
        task_id = args[task_id_index]
        if task_id.isdigit():
            if tasks:
                task_found = False
                for task in tasks:
                    if task["id"] == int(task_id):
                        task_found = True
                        if args[1] == "mark-in-progress":
                            task['status'] = "in-progress"
                        elif args[1] == "mark-done":
                            task['status'] = "done"
                        break

                if task_found:
                    with open("tasks.json", "w") as file:
                        json.dump(tasks, file, indent=4)
            
                    print("Task status updated succesfully.")
                else:
                    print("No task found with given ID.")
        else:
            print("Task ID can only be a number.")

        