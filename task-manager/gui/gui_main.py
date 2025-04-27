from tkinter import *
from tasks.task_manager import TaskManager

manager = TaskManager()

# Monkey-patch: Add rounded rectangle support to Canvas
def _create_round_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

Canvas.create_round_rectangle = _create_round_rectangle

def show_task_input(task_name_entry, task_input_button):
    task_name_entry.pack(pady=100)
    task_input_button.pack_forget()

def add_task(task_name_entry, task_list_canvas, task_input_button):
    task_name = task_name_entry.get().strip()
    if task_name:
        manager.add_task(task_name)
        update_task_display(task_list_canvas, task_input_button, task_name_entry)
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_input_button.pack_forget()

def cancel_task_input(task_name_entry, task_input_button):
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_input_button.pack_forget()

def delete_task(index, task_list_canvas, task_input_button, task_name_entry):
    del manager.tasks[index]
    update_task_display(task_list_canvas, task_input_button, task_name_entry)

def update_task_display(canvas, task_input_button, task_name_entry):
    canvas.delete("all")  # Clear existing items

    y = 10  # Starting y position
    for index, task in enumerate(manager.tasks):
        text = f"{task.description}"

        canvas.create_round_rectangle(10, y, 480, y + 40, radius=5, fill="#F4F1DE")
        canvas.create_text(30, y + 20, anchor="w", text=text, font=("Arial", 12), fill="#3D405B")

        # Create the delete button for this task
        delete_button = Button(canvas, text="X", font=("Arial", 10, "bold"), fg="white", bg="#E07A5F",
                               command=lambda idx=index: delete_task(idx, canvas, task_input_button, task_name_entry))
        canvas.create_window(450, y + 20, window=delete_button)

        y += 50  # Increment y to position the next task

    # Reposition the Add Task button below the last task
    canvas.create_window(250, y + 25, window=task_input_button)

def run_gui():
    window = Tk()
    window.title("Task Manager")
    window.geometry("500x600")
    window.configure(bg="#81B29A")
    window.resizable(False, False)

    title_label = Label(window, text="Your Task Manager", font=("Arial", 18, "bold"), fg="#3D405B", bg="#81B29A")
    title_label.pack(pady=10)

    task_name_entry = Entry(window, width=40)

    canvas_frame = Frame(window)
    canvas_frame.pack(pady=10, fill="both", expand=True)

    task_list_canvas = Canvas(canvas_frame, bg="#81B29A", highlightthickness=0)
    task_list_canvas.pack(fill="both", expand=True)

    task_add_button = Button(window, text="Add Task", command=lambda: show_task_input(task_name_entry, task_add_button))
    task_add_button.config(font=("Arial", 12, "bold"), fg="#3D405B", bg="#F4F1DE")

    task_name_entry.bind('<Return>', lambda event: add_task(task_name_entry, task_list_canvas, task_add_button))
    task_name_entry.bind('<Escape>', lambda event: cancel_task_input(task_name_entry, task_add_button))

    update_task_display(task_list_canvas, task_add_button, task_name_entry)

    window.mainloop()
