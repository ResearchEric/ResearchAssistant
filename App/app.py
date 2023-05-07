import os
import time
from typing import List
from dotenv import load_dotenv
from task_manager import TaskManager

load_dotenv()

OBJECTIVE = os.getenv(
    "OBJECTIVE", "This is a user prompt that will spawn a task list based off agent behavior")

INITIAL_TASK = os.getenv("INITIAL_TASK\", "Develop a task list")

task_list = [{"task_name": INITIAL_TASK}]

task_manager = TaskManager()

while True:
    print("\n----------------------- Task List -----------------------")
    for i, task in enumerate(task_list):
        print(f"{i + 1}. {task['task_name']}")

    print("Enter 's' to save and exit.")
    print("Enter 'e' to exit without saving.")
    print("Enter a number to automatically process tasks for X hours.")

    user_input = input("Enter your action: ")

    if user_input.isdigit():
        hours = float(user_input)
        task_manager.process_tasks_for_x_hours(
            task_list, OBJECTIVE, hours)

    elif user_input == "s":
        task_manager.save_and_exit(task_list)
        break

    elif user_input == "e":
        task_manager.exit_without_saving()
        break

    else:
        task_manager.process_tasks(task_list, OBJECTIVE)
