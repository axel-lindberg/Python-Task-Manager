import json
import os
from .task import Task
from .task_with_status import TaskWithStatus

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(TaskWithStatus(task))  # Lägg till som TaskWithStatus direkt
        self.save_tasks()
        return task

    def list_tasks(self):
        return [str(task_with_status.task) for task_with_status in self.tasks]

    def save_tasks(self):
        data = []
        for task_with_status in self.tasks:
            task_data = {
                "description": task_with_status.task.description,
                "completed": task_with_status.completed,
                "due_date": task_with_status.due_date
            }
            data.append(task_data)

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r") as f:
            data = json.load(f)

        for task_data in data:
            task = Task(task_data["description"])
            wrapped = TaskWithStatus(task)
            wrapped.completed = task_data.get("completed", False)
            wrapped.due_date = task_data.get("due_date", None)
            self.tasks.append(wrapped)
