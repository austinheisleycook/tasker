import sqlite3
import tkinter as tk
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tasks.db"


def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


class Tasker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tasker")
        self.geometry("500x400")
        create_database()

        self.lbltitle = tk.Label(text="Title")
        self.lbltitle.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.txttitle = tk.Entry(width=50)
        self.txttitle.grid(row=1, column=0, padx=10)

        self.lbldescription = tk.Label(text="Description")
        self.lbldescription.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.txtdescription = tk.Entry(width=50)
        self.txtdescription.grid(row=3, column=0, padx=10)

        self.btnaddtask = tk.Button(text="Add Task", command=self.AddEntry)
        self.btnaddtask.grid(row=4, column=0, pady=10)

        self.lbltasks = tk.Label(text="Tasks")
        self.lbltasks.grid(row=5, column=0, sticky="w", padx=10)

        self.task_frame = tk.Frame(self)
        self.task_frame.grid(row=6, column=0, padx=10, pady=(5, 10), sticky="nsew")

        self.RefreshTasks()

    def AddEntry(self):
        title = self.txttitle.get().strip()
        description = self.txtdescription.get().strip()

        if not title or not description:
            return

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description),
            )

        self.txttitle.delete(0, tk.END)
        self.txtdescription.delete(0, tk.END)
        self.RefreshTasks()

    def RefreshTasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        with sqlite3.connect(DB_PATH) as connection:
            tasks = connection.execute(
                "SELECT title, description FROM tasks ORDER BY id DESC"
            ).fetchall()

        if not tasks:
            tk.Label(self.task_frame, text="No tasks yet", fg="gray").pack(pady=5)
            return

        for row, (title, description) in enumerate(tasks):
            task_label = tk.Label(
                self.task_frame,
                text=f"{title} - {description}",
                anchor="w",
                justify="left",
                padx=8,
                pady=5,
                relief="groove",
            )
            task_label.grid(row=row, column=0, sticky="ew", pady=2)


if __name__ == "__main__":
    tasker = Tasker()
    tasker.mainloop()