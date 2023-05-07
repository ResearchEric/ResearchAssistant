import time
from typing import List
from agents.task_creation_agent import task_creation_agent
from agents.prioritization_agent import prioritization_agent
from agents.execution_agent import execution_agent
from agents.context_agent import context_agent
from agents.html_documentation_agent import html_documentation_agent
from agents.openai_call import openai_call


class TaskManager:
    def __init__(self, objective: str, task_list: List) -> None:
        self.objective = objective
        self.task_list = task_list
        self.context = context_agent(
            objective=self.objective, task_list=self.task_list)

    def process_tasks(self) -> None:
        self._execute_tasks()
        self._generate_documentation()
        self._check_task_completion()

    def process_tasks_for_x_hours(self, hours: float) -> None:
        end_time = time.time() + hours * 3600
        print(f"\nProcessing tasks for {hours} hours. Timer started.")
        while time.time() < end_time:
            self._execute_tasks()
            if not self.task_list:
                print("\nAll tasks completed. Exiting...")
                break

    def save_and_exit(self) -> None:
        self._generate_documentation()
        self._write_documentation_to_file()
        print("\nTask list saved. Exiting...")

    def exit_without_saving(self) -> None:
        print("\nExiting without saving...")

    def _execute_tasks(self) -> None:
        new_tasks = task_creation_agent(
            objective=self.objective, result=self.context, task_description="Develop a task list", task_list=self.task_list)
        self.task_list.extend(new_tasks)
        prioritized_tasks = prioritization_agent(
            objective=self.objective, task_list=self.task_list)

        for task in prioritized_tasks:
            print(f"\nExecuting task: {task['task_name']}")
            execution_result = execution_agent(
                task_description=task["task_name"], context=self.context)
            print(f"Task result: {execution_result}")

            if "completed" in execution_result and execution_result["completed"]:
                self.task_list.remove(task)

    def _generate_documentation(self) -> None:
        documentation_text = html_documentation_agent(
            objective=self.objective, context=self.context, task_list=self.task_list)
        return documentation_text

    def _check_task_completion(self) -> None:
        if not self.task_list:
            print("\nAll tasks completed. Exiting...")

    def _write_documentation_to_file(self) -> None:
        documentation_text = self._generate_documentation()
        with open("documentation.html", "w") as file:
            file.write(documentation_text)
