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
        self.geometry("680x620")
        self.minsize(560, 500)
        create_database()

        # Calm, modern color palette
        self.colors = {
            "bg": "#F4F6FB",
            "surface": "#FFFFFF",
            "surface_alt": "#F8FAFD",
            "primary": "#5B6CFF",
            "primary_hover": "#4A5AE8",
            "text": "#1F2430",
            "muted": "#7A8194",
            "border": "#E7EAF2",
            "danger": "#E66A6A",
        }

        self.configure(bg=self.colors["bg"])
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=self.colors["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=32, pady=(24, 18))
        header.columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="Tasker",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="A simple, focused space for your to-do list",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        content = tk.Frame(self, bg=self.colors["bg"])
        content.grid(row=1, column=0, sticky="nsew", padx=32, pady=(0, 28))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        composer = tk.Frame(
            content,
            bg=self.colors["surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        composer.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        composer.columnconfigure(0, weight=1)

        inner = tk.Frame(composer, bg=self.colors["surface"])
        inner.grid(row=0, column=0, sticky="ew", padx=18, pady=18)
        inner.columnconfigure(0, weight=1)

        tk.Label(
            inner,
            text="Create a task",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["text"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        self.lbltitle = tk.Label(
            inner,
            text="Title",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["muted"],
        )
        self.lbltitle.grid(row=1, column=0, sticky="w")

        self.txttitle = tk.Entry(
            inner,
            font=("Segoe UI", 11),
            bg=self.colors["surface_alt"],
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            insertbackground=self.colors["text"],
        )
        self.txttitle.grid(row=2, column=0, sticky="ew", ipady=8, pady=(5, 10))

        self.lbldescription = tk.Label(
            inner,
            text="Description",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["muted"],
        )
        self.lbldescription.grid(row=3, column=0, sticky="w")

        self.txtdescription = tk.Entry(
            inner,
            font=("Segoe UI", 11),
            bg=self.colors["surface_alt"],
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            insertbackground=self.colors["text"],
        )
        self.txtdescription.grid(row=4, column=0, sticky="ew", ipady=8, pady=(5, 12))

        action_row = tk.Frame(inner, bg=self.colors["surface"])
        action_row.grid(row=5, column=0, sticky="ew")
        action_row.columnconfigure(0, weight=1)

        self.status_label = tk.Label(
            action_row,
            text="",
            font=("Segoe UI", 9),
            bg=self.colors["surface"],
            fg=self.colors["muted"],
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.btnaddtask = tk.Button(
            action_row,
            text="  + Add task  ",
            command=self.AddEntry,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_hover"],
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=8,
        )
        self.btnaddtask.grid(row=0, column=1)

        list_container = tk.Frame(
            content,
            bg=self.colors["surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        list_container.grid(row=1, column=0, sticky="nsew")
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(1, weight=1)

        list_header = tk.Frame(list_container, bg=self.colors["surface"])
        list_header.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 8))
        list_header.columnconfigure(0, weight=1)

        self.lbltasks = tk.Label(
            list_header,
            text="My tasks",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["surface"],
            fg=self.colors["text"],
        )
        self.lbltasks.grid(row=0, column=0, sticky="w")

        self.task_count = tk.Label(
            list_header,
            text="0 tasks",
            font=("Segoe UI", 9),
            bg=self.colors["surface"],
            fg=self.colors["muted"],
        )
        self.task_count.grid(row=0, column=1, sticky="e")

        self.task_frame = tk.Frame(list_container, bg=self.colors["surface"])
        self.task_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(4, 16))
        self.task_frame.columnconfigure(0, weight=1)

        self.txttitle.bind("<Return>", lambda event: self.txtdescription.focus_set())
        self.txtdescription.bind("<Return>", lambda event: self.AddEntry())

        self.RefreshTasks()

    def AddEntry(self):
        title = self.txttitle.get().strip()
        description = self.txtdescription.get().strip()

        if not title or not description:
            self.status_label.config(text="Add a title and description")
            return

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description),
            )

        self.txttitle.delete(0, tk.END)
        self.txtdescription.delete(0, tk.END)
        self.status_label.config(text="Task added")
        self.txttitle.focus_set()
        self.RefreshTasks()

    def RefreshTasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        with sqlite3.connect(DB_PATH) as connection:
            tasks = connection.execute(
                "SELECT id, title, description FROM tasks ORDER BY id DESC"
            ).fetchall()

        count = len(tasks)
        self.task_count.config(text=f"{count} {'task' if count == 1 else 'tasks'}")

        if not tasks:
            empty = tk.Frame(
                self.task_frame,
                bg=self.colors["surface_alt"],
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )
            empty.grid(row=0, column=0, sticky="ew", pady=8)
            tk.Label(
                empty,
                text="No tasks yet",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["surface_alt"],
                fg=self.colors["text"],
            ).pack(pady=(18, 2))
            tk.Label(
                empty,
                text="Add your first task above",
                font=("Segoe UI", 9),
                bg=self.colors["surface_alt"],
                fg=self.colors["muted"],
            ).pack(pady=(0, 18))
            return

        for row, (task_id, title, description) in enumerate(tasks):
            card = tk.Frame(
                self.task_frame,
                bg=self.colors["surface_alt"],
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )
            card.grid(row=row, column=0, sticky="ew", pady=4)
            card.columnconfigure(0, weight=1)

            text_area = tk.Frame(card, bg=self.colors["surface_alt"])
            text_area.grid(row=0, column=0, sticky="ew", padx=(14, 8), pady=12)
            text_area.columnconfigure(0, weight=1)

            tk.Label(
                text_area,
                text=title,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                justify="left",
                bg=self.colors["surface_alt"],
                fg=self.colors["text"],
            ).grid(row=0, column=0, sticky="ew")

            tk.Label(
                text_area,
                text=description,
                font=("Segoe UI", 9),
                anchor="w",
                justify="left",
                wraplength=420,
                bg=self.colors["surface_alt"],
                fg=self.colors["muted"],
            ).grid(row=1, column=0, sticky="ew", pady=(3, 0))

            delete_button = tk.Button(
                card,
                text="Delete",
                command=lambda task_id=task_id: self.DeleteTask(task_id),
                font=("Segoe UI", 9, "bold"),
                bg=self.colors["surface_alt"],
                fg=self.colors["danger"],
                activebackground="#FBECEC",
                activeforeground=self.colors["danger"],
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=12,
                pady=6,
            )
            delete_button.grid(row=0, column=1, padx=(0, 10), pady=8)

    def DeleteTask(self, task_id):
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        self.RefreshTasks()


if __name__ == "__main__":
    tasker = Tasker()
    tasker.mainloop()