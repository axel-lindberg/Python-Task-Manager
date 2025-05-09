import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from tasks.task_manager import TaskManager
from tasks.task_with_status import TaskWithStatus
from tkinter import ttk

manager = TaskManager()

# -------------------- Countdown Timer Class -------------------- #
class CountdownTimer:
    """
    A class to handle a Pomodoro-style countdown timer for study sessions.
    """

    def __init__(self, label, stop_btn, on_finish=None):
        """
        Initializes the countdown timer.
        :param label: The label widget used to display the countdown.
        :param stop_btn: The button widget to toggle between Stop/Resume.
        :param on_finish: Callback function triggered when the timer ends.
        """
        self.label = label
        self.stop_btn = stop_btn
        self.on_finish = on_finish
        self.total_seconds = 0
        self.remaining_seconds = 0
        self._job = None
        self.running = False
        self.paused = False

    def start(self, minutes=None):
        """
        Starts or resumes the countdown timer.
        :param minutes: Duration of the timer in minutes.
        """
        if not self.running and not self.paused:
            self.total_seconds = int(float(minutes) * 60)
            self.remaining_seconds = self.total_seconds
        self.running = True
        self.paused = False
        self._countdown()
        self.stop_btn.config(text="Stop", command=self.stop)

    def _countdown(self):
        """Private recursive method that updates the countdown every second."""
        if self.remaining_seconds > 0 and self.running:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_seconds -= 1
            self._job = self.label.after(1000, self._countdown)
        else:
            if self.remaining_seconds <= 0:
                self.label.config(text="Time's up!")
                if self.on_finish:
                    self.on_finish()
            self.running = False
            self.paused = False
            self.stop_btn.config(text="Stop", command=self.stop)

    def stop(self):
        """Pauses the countdown timer."""
        if self._job:
            self.label.after_cancel(self._job)
            self._job = None
        self.running = False
        self.paused = True
        self.stop_btn.config(text="Resume", command=self.resume)

    def resume(self):
        """Resumes the countdown timer from paused state."""
        if self.paused:
            self.running = True
            self.paused = False
            self._countdown()
            self.stop_btn.config(text="Stop", command=self.stop)

    def reset(self):
        """Resets the timer to its initial state."""
        if self._job:
            self.label.after_cancel(self._job)
        self.label.config(text="00:00")
        self._job = None
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.stop_btn.config(text="Stop", command=self.stop)

# -------------------- Task Manager GUI Functions -------------------- #

# Extend Canvas to draw rounded rectangles
def _create_round_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
    """
    Draws a rounded rectangle on the canvas.
    """
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
    """
    Displays input field for entering a new task name.
    """
    task_name_entry.pack()
    task_add_button.pack_forget()

    def open_calendar_after_input(event=None):
        open_calendar(task_name_entry, task_list_canvas, task_add_button, task_name_entry)

    task_name_entry.bind("<Return>", open_calendar_after_input)
    task_name_entry.bind("<Escape>", lambda e: cancel_task_input(task_name_entry, task_add_button))


def open_calendar(task_name_entry, task_list_canvas, task_add_button, task_name_entry_ref):
    """
    Opens a calendar pop-up to select a due date after entering a task.
    """
    top = Toplevel()
    top.title("Välj Datum")
    top.geometry("300x300")
    top.configure(bg="#81B29A")
    top.resizable(False, False)

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
    """
    Adds a new task with optional due date.
    """
    task_name = task_name_entry.get().strip()
    if task_name:
        task = manager.add_task(task_name)
        manager.tasks[-1] = TaskWithStatus(task, due_date)
        update_task_display(task_list_canvas, task_add_button, task_name_entry_ref)
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_add_button.pack_forget()


def cancel_task_input(task_name_entry, task_add_button):
    """
    Cancels the task input and hides the input field.
    """
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_add_button.pack_forget()


def delete_task(index, task_list_canvas, task_add_button, task_name_entry):
    """
    Deletes a task by index.
    """
    del manager.tasks[index]
    manager.save_tasks()
    update_task_display(task_list_canvas, task_add_button, task_name_entry)


def toggle_task_status(task_with_status, task_list_canvas, task_add_button, task_name_entry):
    """
    Marks a task as complete/incomplete and updates UI.
    """
    task_with_status.completed = not task_with_status.completed
    manager.tasks.sort(key=lambda t: t.completed)
    manager.save_tasks()
    update_task_display(task_list_canvas, task_add_button, task_name_entry)

def edit_task(index, task_list_canvas, task_add_button, task_name_entry):
    """
    Opens a pop-up window to edit a task's description and due date.
    """
    task_with_status = manager.tasks[index]
    task = task_with_status.task

    edit_window = Toplevel()
    edit_window.title("Redigera Task")
    edit_window.geometry("300x400")
    edit_window.configure(bg="#81B29A")
    edit_window.resizable(False, False)

    Label(edit_window, text="Redigera beskrivning:", bg="#81B29A", fg="#3D405B", font=("Arial", 10, "bold")).pack(pady=10)
    desc_entry = Entry(edit_window, width=30)
    desc_entry.insert(0, task.description)
    desc_entry.pack()

    Label(edit_window, text="Välj nytt datum:", bg="#81B29A", fg="#3D405B", font=("Arial", 10, "bold")).pack(pady=10)
    cal = Calendar(edit_window, selectmode='day')
    cal.pack(pady=5)

    def save_changes():
        new_desc = desc_entry.get().strip()
        new_date = cal.selection_get().strftime("%Y-%m-%d")

        if new_desc:
            task.description = new_desc
            task_with_status.due_date = new_date
            manager.save_tasks()
            update_task_display(task_list_canvas, task_add_button, task_name_entry)
            edit_window.destroy()

    Button(edit_window, text="Spara", command=save_changes, bg="#F4F1DE", fg="#3D405B", font=("Arial", 10, "bold")).pack(pady=10)

def update_task_display(canvas, task_input_button, task_name_entry):
    """
    Refreshes the task list display with current tasks and their statuses.
    """
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

        # Checkbox to toggle task complete
        var = BooleanVar(value=completed)
        checkbox = Checkbutton(canvas, variable=var, bg=bg_color, activebackground=bg_color,
                               command=lambda t=task_with_status: toggle_task_status(t, canvas, task_input_button, task_name_entry))
        canvas.create_window(420, y + 25, window=checkbox)

        # Delete and Edit buttons
        delete_button = Button(canvas, text="X", font=("Arial", 10, "bold"), fg="white", bg="#E07A5F",
                               command=lambda idx=index: delete_task(idx, canvas, task_input_button, task_name_entry))
        canvas.create_window(460, y + 25, window=delete_button)

        edit_button = Button(canvas, text="Edit", font=("Arial", 9), bg="#F2CC8F", fg="#3D405B",
                             command=lambda idx=index: edit_task(idx, canvas, task_input_button, task_name_entry))
        canvas.create_window(390, y + 25, window=edit_button)

        y += 60

    # Add task entry/button at the end of the list
    canvas.create_window(250, y + 25, window=task_input_button)
    canvas.create_window(250, y + 25, window=task_name_entry)


# -------------------- Main GUI Function -------------------- #

def run_gui():
    """
    Main function to run the Task Manager GUI.
    """
    window = Tk()
    window.title("Task Manager")
    window.geometry("500x700")
    window.configure(bg="#81B29A")
    window.resizable(False, False)

    # Title
    title_label = Label(window, text="Your Task Manager", font=("Arial", 18, "bold"), fg="#3D405B", bg="#81B29A")
    title_label.pack(pady=10)

    task_name_entry = Entry(window, width=40)

    # Task list area
    canvas_frame = Frame(window)
    canvas_frame.pack(pady=10, fill="both", expand=True)

    task_list_canvas = Canvas(canvas_frame, bg="#81B29A", highlightthickness=0)
    task_list_canvas.pack(fill="both", expand=True)

    task_add_button = Button(window, text="Add Task", command=lambda: show_task_input(task_name_entry, task_list_canvas, task_add_button))
    task_add_button.config(font=("Arial", 12, "bold"), fg="#3D405B", bg="#F4F1DE")

    update_task_display(task_list_canvas, task_add_button, task_name_entry)

    # ---------- Study Timer UI ---------- #
    Label(window, text="Study Timer (minutes)", font=("Arial", 12, "bold"), bg="#81B29A", fg="#3D405B").pack(pady=5)

    timer_frame = Frame(window, bg="#81B29A")
    timer_frame.pack(pady=5)

    duration_var = StringVar(value="25")
    Entry(timer_frame, textvariable=duration_var, width=5, font=("Arial", 12)).grid(row=0, column=0, padx=5)

    timer_label = Label(timer_frame, text="00:00", font=("Arial", 18, "bold"), bg="#81B29A", fg="#3D405B")
    timer_label.grid(row=0, column=1, padx=10)

    stop_btn = Button(timer_frame, text="Stop", bg="#F4F1DE", fg="#3D405B", font=("Arial", 10, "bold"))
    stop_btn.grid(row=0, column=2, padx=5)

    def timer_finished():
        messagebox.showinfo("Study session complete", "Great job! Time's up!")

    countdown_timer = CountdownTimer(label=timer_label, stop_btn=stop_btn, on_finish=timer_finished)

    Button(timer_frame, text="Start", command=lambda: countdown_timer.start(duration_var.get()),
           bg="#F4F1DE", fg="#3D405B", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)

    Button(timer_frame, text="Reset", command=countdown_timer.reset,
           bg="#F4F1DE", fg="#3D405B", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)

    window.mainloop()

# Run the application if this script is executed directly
if __name__ == "__main__":
    run_gui()
