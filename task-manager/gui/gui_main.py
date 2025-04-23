# gui/gui_main.py
from tkinter import *

tasks = []

def show_task_input(task_name_entry, task_input_button, task_list_label):
    task_name_entry.pack(pady=5)
    task_input_button.pack_forget()  # Hide the "Add Task" button once pressed

def add_task(task_name_entry, task_list_label, task_input_button):
    task_name = task_name_entry.get()

    if task_name.strip():
        tasks.append(task_name)
        update_task_display(task_list_label)

    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_input_button.pack(pady=20)

def cancel_task_input(task_name_entry, task_input_button):
    task_name_entry.delete(0, END)
    task_name_entry.pack_forget()
    task_input_button.pack(pady=20)

def update_task_display(task_list_label):
    # Clear the current displayed tasks
    task_list_label.config(text="")

    # Display each task in the list
    for task in tasks:
        task_list_label.config(text=task_list_label.cget("text") + task + "\n")

def run_gui():
    window = Tk()
    window.title("Task Manager")
    window.geometry("500x600")
    window.configure(bg="lightgray")
    window.resizable(False, False)

    title_label = Label(window, text="Task Manager", font=("Arial", 18), bg="lightgray")
    title_label.pack(pady=20)

    # Task Name Input
    task_name_entry = Entry(window, width=40)

    # Button to show task input field
    task_input_button = Button(window, text="Add Task", command=lambda: show_task_input(task_name_entry, task_input_button, task_list_label))

    # Task List Display
    task_list_label = Label(window, text="", bg="lightgray")
    task_list_label.pack(pady=10)

    # Bind the Enter key to add the task when pressed
    task_name_entry.bind('<Return>', lambda event: add_task(task_name_entry, task_list_label, task_input_button))

    # Cancel if nothing typed in the entry field
    task_name_entry.bind('<Escape>', lambda event: cancel_task_input(task_name_entry, task_input_button))

    task_input_button.pack(pady=20)

    window.mainloop()
