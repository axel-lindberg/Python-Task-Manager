class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def update_description(self, new_description):
        self.description = new_description

    def __str__(self):
        status = "✔" if self.completed else "✘"
        return f"[{status}] {self.description}"