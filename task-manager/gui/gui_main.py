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
    for widget in task_list_label.winfo_children():
        widget.destroy()

    # Display each task with a colored background
    for task in tasks:
        task_label = Label(task_list_label, text=task, bg="lightblue", font=("Arial", 12), relief="solid", padx=10, pady=5)
        task_label.pack(pady=5, fill="x")

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

    # Task List Display (this will contain task labels)
    task_list_label = Frame(window, bg="lightgray")
    task_list_label.pack(pady=10, fill="both", expand=True)

    # Bind the Enter key to add the task when pressed
    task_name_entry.bind('<Return>', lambda event: add_task(task_name_entry, task_list_label, task_input_button))

    # Cancel if nothing typed in the entry field
    task_name_entry.bind('<Escape>', lambda event: cancel_task_input(task_name_entry, task_input_button))

    task_input_button.pack(pady=20)

    window.mainloop()
