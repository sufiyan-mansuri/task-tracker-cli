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
- Graceful error handling for missing arguments, invalid IDs, unknown commands, and a missing/corrupted `tasks.json`

## Requirements

- Python 3
- No external libraries — only the standard library (`sys`, `os`, `json`, `datetime`)

## Usage

Run the script with `python main.py` followed by a command.

### Add a task

```bash
python main.py add "Buy groceries"
# Task added successfully (ID: 1)
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
| `createdAt` | ISO 8601 timestamp when the task was created  |
| `updatedAt` | ISO 8601 timestamp when the task was last updated |

## Data storage

Tasks are stored in a `tasks.json` file in the directory the script is run from. This file is created automatically the first time you add a task.

## Design notes

A few implementation details worth knowing if you're reading this as a reference:

- **IDs are `max(existing_ids) + 1`, not `len(tasks) + 1`.** Using the list length breaks once a task has been deleted — you can end up assigning an ID that's already in use. Taking the max avoids that.
- **Every command validates its own arguments before touching `tasks.json`** (missing description, missing ID, non-numeric ID, unknown status filter) so a bad command prints a clear message instead of crashing with a traceback.
- **`load_tasks()` never raises on a missing or corrupted file** — a missing `tasks.json` is treated as "no tasks yet," and invalid JSON in the file prints a warning and falls back to an empty list rather than crashing.
- **Commands are dispatched through a dictionary (`COMMANDS`)** mapping command name → handler function, instead of a long `if/elif` chain. This makes it easy to add a new command later without touching existing logic.

## License

MIT