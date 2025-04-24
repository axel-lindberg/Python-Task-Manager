from .task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        self.tasks.append(Task(description))

    def list_tasks(self):
        return [str(task) for task in self.tasks]