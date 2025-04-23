from .task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        self.tasks.append(Task(description))

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def mark_task_incomplete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_incomplete()

    def edit_task_description(self, index, new_description):
        if 0 <= index < len(self.tasks):
            self.tasks[index].update_description(new_description)

    def move_task(self, from_index, to_index):
        if (0 <= from_index < len(self.tasks)) and (0 <= to_index < len(self.tasks)):
            task = self.tasks.pop(from_index)
            self.tasks.insert(to_index, task)

    def list_tasks(self):
        return [(i, str(task)) for i, task in enumerate(self.tasks)]