from typing import Dict, List
from agents.openai_call import openai_call

TASK_NAME_KEY = "task_name"


def task_creation_agent(objective: str, result: Dict, task_description: str, task_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    prompt = f"""
You are a task creation agent. Your objective is to create new tasks based on the current result and the task list.
Objective: {objective}
Result: {result}
Task description: {task_description}
Task list: {task_list}
Create a new task and return it in the following format:
{{
    "{TASK_NAME_KEY}": "Task description"
}}
"""

    # Call openai API to get response
    response = openai_call(prompt, max_tokens=2000)

    # Use list comprehension and one liner to parse output
    new_tasks = [{TASK_NAME_KEY: task.strip()}
                 for task in response.strip().split('\n')]

    return new_tasks
