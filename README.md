# Tasker

Tasker is a simple desktop to-do application built with Python and the Tkinter GUI toolkit. It lets you create tasks with a title and description, view saved tasks in a modern task list, and delete tasks you no longer need.

## Features

- Create a task with a title and description
- Automatically save tasks in a local SQLite database
- Display tasks from newest to oldest
- Show the total number of tasks
- Delete individual tasks
- Retain tasks between application sessions
- Submit a task with the **Add task** button or Enter key

## Requirements

- Python 3
- Tkinter, which is included with many standard Python installations

## Run the Program

From the project directory, run:

```bash
python app.py
```

A Tasker window will open. The application will create `tasks.db` automatically if it does not already exist.

## How to Use It

1. Enter a task title in the **Title** field.
2. Enter details in the **Description** field.
3. Click **Add task** or press Enter.
4. The task appears in **My tasks**.
5. Click **Delete** beside a task to remove it.

Both the title and description are required. If either field is empty, the application displays a prompt and does not save the task.

## Project Files

- `app.py` — Contains the Tkinter interface and task-management logic.
- `tasks.db` — SQLite database containing saved tasks.
- `readme.md` — Project documentation.

## Database

Tasker uses SQLite and stores the database in the same directory as `app.py`. On startup, it creates a `tasks` table if it does not exist:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Each task has:

- `id` — Unique database identifier
- `title` — Task title
- `description` — Task details
- `created_at` — Timestamp assigned by SQLite when the task is added

## Application Structure

The main `Tasker` class creates the window, composer form, task list, status messages, and delete controls. The main database operations are:

- `create_database()` — Creates the database table
- `AddEntry()` — Validates and inserts a new task
- `RefreshTasks()` — Reloads and displays saved tasks
- `DeleteTask(task_id)` — Deletes a task by its ID
