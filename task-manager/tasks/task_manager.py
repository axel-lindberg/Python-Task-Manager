import json
import os
from .task import Task
from .task_with_status import TaskWithStatus

class TaskManager:
    def __init__(self):
        """
        Initializes a TaskManager instance.
        Loads tasks from the JSON file into memory.
        """
        self.tasks = []  # List to hold TaskWithStatus objects
        self.filename = "tasks.json"  # File to store task data
        self.load_tasks()  # Load existing tasks from file

    def add_task(self, description):
        """
        Adds a new task with the given description.
        The task is wrapped in a TaskWithStatus object and saved.

        :param description: Description of the task
        :return: The Task object that was added
        """
        task = Task(description)  # Create a basic Task object
        self.tasks.append(TaskWithStatus(task))  # Wrap with status and add to list
        self.save_tasks()  # Save updated task list to file
        return task

    def list_tasks(self):
        """
        Returns a list of task descriptions (without status or date).

        :return: List of task descriptions as strings
        """
        return [str(task_with_status.task) for task_with_status in self.tasks]

    def save_tasks(self):
        """
        Saves the current tasks to a JSON file.
        Stores task description, completion status, and due date.
        """
        data = []
        for task_with_status in self.tasks:
            task_data = {
                "description": task_with_status.task.description,
                "completed": task_with_status.completed,
                "due_date": task_with_status.due_date
            }
            data.append(task_data)

        # Write the data list to the file in JSON format
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        """
        Loads tasks from the JSON file into memory.
        If the file doesn't exist, nothing is loaded.
        """
        if not os.path.exists(self.filename):
            return  # Do nothing if file doesn't exist

        with open(self.filename, "r") as f:
            data = json.load(f)  # Read and parse JSON

        # Convert each dictionary from the file into a TaskWithStatus object
        for task_data in data:
            task = Task(task_data["description"])
            wrapped = TaskWithStatus(task)
            wrapped.completed = task_data.get("completed", False)
            wrapped.due_date = task_data.get("due_date", None)
            self.tasks.append(wrapped)
