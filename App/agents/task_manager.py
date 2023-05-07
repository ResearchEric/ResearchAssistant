import time
from typing import List
from agents.task_creation_agent import task_creation_agent
from agents.prioritization_agent import prioritization_agent
from agents.execution_agent import execution_agent
from agents.context_agent import context_agent
from agents.html_documentation_agent import html_documentation_agent


class TaskManager:
    def process_tasks(self, task_list: List, objective: str) -> None:
        self._execute_tasks(task_list, objective)
        self._generate_documentation(task_list, objective)
        self._check_task_completion(task_list)

    def process_tasks_for_x_hours(self, task_list: List, objective: str, hours: float) -> None:
        end_time = time.time() + hours * 3600
        print(f"\nProcessing tasks for {hours} hours. Timer started.")
        while time.time() < end_time:
            self._execute_tasks(task_list, objective)
            if not task_list:
                print("\nAll tasks completed. Exiting...")
                break

    def save_and_exit(self, task_list: List, objective: str) -> None:
        self._generate_documentation(task_list, objective)
        print("\nTask list saved. Exiting...")

    def exit_without_saving(self) -> None:
        print("\nExiting without saving...")

    def _execute_tasks(self, task_list: List, objective: str) -> None:
        context = context_agent(objective=objective, task_list=task_list)
        new_tasks = task_creation_agent(
            objective=objective, result=context, task_description="Develop a task list", task_list=task_list)
        task_list.extend(new_tasks)
        prioritized_tasks = prioritization_agent(task_list=task_list)

        for task in prioritized_tasks:
            print(f"\nExecuting task: {task['task_name']}")
            execution_result = execution_agent(
                task_description=task["task_name"], context=context)
            print(f"Task result: {execution_result}")

            if "completed" in execution_result and execution_result["completed"]:
                task_list.remove(task)

    def _generate_documentation(self, task_list: List, objective: str) -> None:
        context = context_agent(objective=objective, task_list=task_list)
        documentation_text = html_documentation_agent(
            objective=objective, context=context, task_list=task_list)
        self._write_documentation_to_file(documentation_text)

    def _check_task_completion(self, task_list: List) -> None:
        if not task_list:
            print("\nAll tasks completed. Exiting...")

    @staticmethod
    def _write_documentation_to_file(documentation_text: str) -> None:
        with open("documentation.html", "w") as file:
            file.write(documentation_text)
