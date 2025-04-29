class TaskWithStatus:
    def __init__(self, task, due_date=None):
        self.task = task
        self.completed = False
        self.due_date = due_date