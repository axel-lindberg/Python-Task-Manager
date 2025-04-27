from .task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)
        return task

    def list_tasks(self):
        return [str(task) for task in self.tasks]