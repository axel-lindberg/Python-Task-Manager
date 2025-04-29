from tkinter import *
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from tasks.task_manager import TaskManager
from tasks.task_with_status import TaskWithStatus  # Ny fil du nämnde

manager = TaskManager()

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
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

Canvas.create_round_rectangle = _create_round_rectangle

def show_task_input(task_name_entry, task_list_canvas, task_add_button):
    task_name_entry.pack()
    task_add_button.pack_forget()

    def open_calendar_after_input(event=None):
        open_calendar(task_name_entry, task_list_canvas, task_add_button, task_name_entry)

    task_name_entry.bind("<Return>", open_calendar_after_input)
    task_name_entry.bind("<Escape>", lambda e: cancel_task_input(task_name_entry, task_add_button))

def open_calendar(task_name_entry, task_list_canvas, task_add_button, task_name_entry_ref):
    top = Toplevel()
    top.title("Välj Datum")
    top.geometry("300x300")
    top.configure(bg="#81B29A")

    cal = Calendar(top, selectmode='day')
    cal.pack(pady=20)

    def select_date():
        selected_date = cal.selection_get()
        task_name = task_name_entry.get().strip()

        if task_name:
            task = manager.add_task(task_name)
            wrapped = TaskWithStatus(task, selected_date.strftime("%Y-%m-%d"))
            manager.tasks[-1] = wrapped
            manager.save_tasks()
            update_task_display(task_list_canvas, task_add_button, task_name_entry_ref)

        task_name_entry.delete(0, END)
        top.destroy()

    select_btn = Button(top, text="Välj Datum", command=select_date, font=("Arial", 12, "bold"), bg="#F4F1DE", fg="#3D405B")
    select_btn.pack(pady=10)

def add_task(task_name_entry, task_list_canvas, task_add_button, task_name_entry_ref, due_date=None):
    task_name = task_name_entry.get().strip()
    if task_name:
        task = manager.add_task(task_name)
        manager.tasks[-1] = TaskWithStatus(task, due_date)
        update_task_display(task_list_canvas, task_add_button, task_name_entry_ref)
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_add_button.pack_forget()

def cancel_task_input(task_name_entry, task_add_button):
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_add_button.pack_forget()

def delete_task(index, task_list_canvas, task_add_button, task_name_entry):
    del manager.tasks[index]
    manager.save_tasks()
    update_task_display(task_list_canvas, task_add_button, task_name_entry)

def toggle_task_status(task_with_status, task_list_canvas, task_add_button, task_name_entry):
    task_with_status.completed = not task_with_status.completed
    manager.tasks.sort(key=lambda t: t.completed)
    update_task_display(task_list_canvas, task_add_button, task_name_entry)

def update_task_display(canvas, task_input_button, task_name_entry):
    canvas.delete("all")

    y = 10
    for index, task_with_status in enumerate(manager.tasks):
        task = task_with_status.task
        completed = task_with_status.completed
        due_date = task_with_status.due_date

        bg_color = "#F4F1DE" if not completed else "#E0DED3"

        canvas.create_round_rectangle(10, y, 480, y + 50, radius=5, fill=bg_color)

        text_options = {"anchor": "w", "font": ("Arial", 12), "fill": "#3D405B"}
        if completed:
            text_options["font"] = ("Arial", 12, "overstrike")

        canvas.create_text(30, y + 15, text=task.description, **text_options)

        if due_date:
            canvas.create_text(30, y + 35, text=f"Due date: {due_date}", anchor="w", font=("Arial", 8), fill="#3D405B")

        var = BooleanVar(value=completed)
        checkbox = Checkbutton(canvas, variable=var, bg=bg_color, activebackground=bg_color,
                               command=lambda t=task_with_status: toggle_task_status(t, canvas, task_input_button, task_name_entry))
        canvas.create_window(420, y + 25, window=checkbox)

        delete_button = Button(canvas, text="X", font=("Arial", 10, "bold"), fg="white", bg="#E07A5F",
                               command=lambda idx=index: delete_task(idx, canvas, task_input_button, task_name_entry))
        canvas.create_window(460, y + 25, window=delete_button)

        y += 60

    canvas.create_window(250, y + 25, window=task_input_button)
    canvas.create_window(250, y + 25, window=task_name_entry)

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

    task_add_button = Button(window, text="Add Task", command=lambda: show_task_input(task_name_entry, task_list_canvas, task_add_button))
    task_add_button.config(font=("Arial", 12, "bold"), fg="#3D405B", bg="#F4F1DE")

    update_task_display(task_list_canvas, task_add_button, task_name_entry)

    window.mainloop()

if __name__ == "__main__":
    run_gui()
