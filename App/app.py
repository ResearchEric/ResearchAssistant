from typing import Dict, List
from agents.context_agent import context_agent
from agents.execution_agent import execution_agent
from agents.html_documentation_agent import html_documentation_agent
from storage.task_manager import load_tasks, save_tasks, save_context_mapping, save_execution_report, save_html_documentation


def main():
    while True:
        print("\n----------------------- Task List -----------------------")
        task_list = load_tasks()
        for i, task in enumerate(task_list):
            print(f"{i + 1}. {task['task_name']}")

        print("Enter 'c' to generate context mapping.")
        print("Enter 'e' to generate execution report.")
        print("Enter 'h' to generate html documentation.")
        print("Enter 's' to save and exit.")
        print("Enter 'e' to exit without saving.")
        print("Enter a number to automatically process tasks for X hours.")

        user_input = input("Enter your action: ")

        if user_input.isdigit():
            hours = float(user_input)
            # call the process_tasks_for_x_hours function from the task_manager module
            task_list = process_tasks_for_x_hours(task_list, hours)

        elif user_input == "c":
            objective = input("Enter the objective of the project: ")
            context = input("Enter the current context of the project: ")
            subject = input("Enter the subject of the project: ")
            # call the context_agent function from the agents module
            context_mapping = context_agent(
                objective, task_list, context, subject)
            # call the save_context_mapping function from the task_manager module
            save_context_mapping(context_mapping)

        elif user_input == "e":
            task_id = input("Enter the ID of the task to execute: ")
            task = get_task_by_id(task_list, task_id)
            # call the execution_agent function from the agents module
            execution_report = execution_agent(task)
            # call the save_execution_report function from the task_manager module
            save_execution_report(execution_report)

        elif user_input == "h":
            objective = input("Enter the objective of the project: ")
            context = input("Enter the current context of the project: ")
            # call the html_documentation_agent function from the agents module
            html_doc = html_documentation_agent(objective, context, task_list)
            # call the save_html_documentation function from the task_manager module
            save_html_documentation(html_doc)

        elif user_input == "s":
            # call the save_tasks function from the task_manager module
            save_tasks(task_list)
            break

        elif user_input == "e":
            exit_without_saving()
            break

        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()
