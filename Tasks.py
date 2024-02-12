import os
import tkinter as tk
from subprocess import Popen

def run_task(task_folder):
    main_py_path = os.path.join(task_folder, "main.py")
    Popen(["python", main_py_path])

def create_main_window(tasks_folder):
    root = tk.Tk()
    root.title("Tasks Runner")
    root.geometry("600x550")  
    root.configure(bg="lightgray")

    label = tk.Label(root, text="DSP TASKS", font=("Helvetica", 22), fg="black", bg="lightblue")
    label.pack(pady=10)

    for task_name in os.listdir(tasks_folder):
        task_folder = os.path.join(tasks_folder, task_name)
        if os.path.isdir(task_folder):
            button = tk.Button(root, text=task_name, command=lambda t=task_folder: run_task(t),
                               width=12, height=1, font=("Helvetica", 14), bg="blue", fg="white")
            button.pack(pady=5)

    root.mainloop()

tasks_folder_path = "D:/FCIS/Projects/4th year/DSP Tasks"
create_main_window(tasks_folder_path)
