import os
import time
from typing import List
from dotenv import load_dotenv
from task_manager import TaskManager


SAVE_AND_EXIT = "s"
EXIT_WITHOUT_SAVING = "e"


def main() -> None:
    load_dotenv()

    OBJECTIVE = os.getenv(
        "OBJECTIVE", "This is a user prompt that will spawn a task list based off agent behavior")
    INITIAL_TASK = os.getenv("INITIAL_TASK", "Develop a task list")

    task_list: List[dict] = [{"task_name": INITIAL_TASK}]
    task_manager = TaskManager()

    while True:
        print_task_list(task_list)

        user_input = input("Enter your action: ")

        if user_input.isdigit():
            hours = float(user_input)
            task_manager.process_tasks_for_x_hours(task_list, OBJECTIVE, hours)
        elif user_input == SAVE_AND_EXIT:
            task_manager.save_and_exit(task_list)
            break
        elif user_input == EXIT_WITHOUT_SAVING:
            task_manager.exit_without_saving()
            break
        else:
            task_manager.process_tasks(task_list, OBJECTIVE)


def print_task_list(task_list: List[dict]) -> None:
    print("\n----------------------- Task List -----------------------")
    for i, task in enumerate(task_list):
        print(f"{i + 1}. {task['task_name']}")

    hours = 0  # Replace with actual value
    print(f"Enter a number to automatically process tasks for {hours} hours.")
    print(f"Enter '{SAVE_AND_EXIT}' to save and exit.")
    print(f"Enter '{EXIT_WITHOUT_SAVING}' to exit without saving.")


if __name__ == "__main__":
    main()
