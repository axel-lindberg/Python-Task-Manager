class Task:
    def __init__(self, description):
        """
        Initializes a Task object.

        :param description: A string describing the task
        """
        self.description = description  # Task description
        self.completed = False  # Task completion status, initially False

    def mark_complete(self):
        """
        Marks the task as completed.
        """
        self.completed = True

    def mark_incomplete(self):
        """
        Marks the task as incomplete.
        """
        self.completed = False

    def update_description(self, new_description):
        """
        Updates the description of the task.

        :param new_description: New string to set as the task description
        """
        self.description = new_description

    def __str__(self):
        """
        Returns a string representation of the task.

        :return: The task's description as a string
        """
        return f"{self.description}"
