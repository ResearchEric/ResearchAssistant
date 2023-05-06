import os
import time
from typing import Dict, List
import openai
from dotenv import load_dotenv
from agents.task_creation_agent import task_creation_agent
from agents.prioritization_agent import prioritization_agent
from agents.execution_agent import execution_agent
from agents.context_agent import context_agent
from agents.html_documentation_agent import html_documentation_agent

load_dotenv()

OBJECTIVE = os.getenv(
    "OBJECTIVE", "This is a user prompt that will spawn a task list based off agent behavior")
INITIAL_TASK = os.getenv("INITIAL_TASK", "Develop a task list")
task_list = [{"task_name": INITIAL_TASK}]

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
        seconds = hours * 3600
        end_time = time.time() + seconds
        print(f"\nProcessing tasks for {hours} hours. Timer started.")
        while time.time() < end_time:
            context = context_agent(objective=OBJECTIVE, task_list=task_list)
            new_tasks = task_creation_agent(
                objective=OBJECTIVE, result=context, task_description=INITIAL_TASK, task_list=task_list)
            task_list.extend(new_tasks)
            prioritized_tasks = prioritization_agent(task_list=task_list)

            for task in prioritized_tasks:
                print(f"\nExecuting task: {task['task_name']}")
                execution_result = execution_agent(
                    task_description=task["task_name"], context=context)
                print(f"Task result: {execution_result}")

                if "completed" in execution_result and execution_result["completed"]:
                    task_list.remove(task)

            documentation_text = html_documentation_agent(
                objective=OBJECTIVE, context=context, task_list=task_list)

        print(f"\nProcessing tasks complete. Exiting...")
        break

    elif user_input == "s":
        with open("task_list.txt", "w") as file:
            for task in task_list:
                file.write(f"{task['task_name']}\n")
        print("\nTask list saved. Exiting...")
        break

    elif user_input == "e":
        print("\nExiting without saving...")
        break

    else:
        context = context_agent(objective=OBJECTIVE, task_list=task_list)
        new_tasks = task_creation_agent(
            objective=OBJECTIVE, result=context, task_description=INITIAL_TASK, task_list=task_list)
        task_list.extend(new_tasks)
        prioritized_tasks = prioritization_agent(task_list=task_list)

        for task in prioritized_tasks:
            print(f"\nExecuting task: {task['task_name']}")
            execution_result = execution_agent(
                task_description=task["task_name"], context=context)
            print(f"Task result: {execution_result}")

            if "completed" in execution_result and execution_result["completed"]:
                task_list.remove(task)

        documentation_text = html_documentation_agent(
            objective=OBJECTIVE, context=context, task_list=task_list)
        with open("documentation.html", "w") as file:
            file.write(documentation_text)

        if not task_list:
            print("\nAll tasks completed. Exiting...")
            break
