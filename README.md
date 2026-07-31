# Task Tracker CLI

A lightweight command-line task tracker built in Python. No external dependencies — just add, update, delete, and track the status of your tasks, with everything saved locally to a `tasks.json` file.

This project is a solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh).

## Features

- Add new tasks
- Update a task's description
- Delete a task
- Mark a task as in-progress or done
- List all tasks, or filter by status (`todo`, `in-progress`, `done`)
- Tasks are persisted locally in `tasks.json`, with `createdAt` and `updatedAt` timestamps

## Requirements

- Python 3

## Usage

Run the script with `python main.py` followed by a command.

### Add a task

```bash
python main.py add "Buy groceries"
```

### List tasks

```bash
python main.py list
```

Filter by status:

```bash
python main.py list todo
python main.py list in-progress
python main.py list done
```

### Update a task

```bash
python main.py update <id> "Updated description"
```

### Mark a task as in-progress or done

```bash
python main.py mark-in-progress <id>
python main.py mark-done <id>
```

### Delete a task

```bash
python main.py delete <id>
```

## Task properties

Each task is stored as a JSON object with the following fields:

| Field       | Description                                  |
|-------------|-----------------------------------------------|
| `id`        | Unique numeric identifier                     |
| `description` | Task description                           |
| `status`    | `todo`, `in-progress`, or `done`              |
| `createdAt` | Timestamp when the task was created           |
| `updatedAt` | Timestamp when the task was last updated      |

## Data storage

Tasks are stored in a `tasks.json` file in the directory the script is run from. This file is created automatically the first time you add a task.

## License

MIT