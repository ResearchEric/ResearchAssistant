from typing import Dict, List
from openai_call import openai_call

TASK_NAME_KEY = "task_name"


def prioritization_agent(objective: str, task_list: List[Dict[str, str]], priorities: Dict[str, str]) -> List[Dict[str, str]]:
    task_descriptions = "\n".join([f"{i+1}. {task[TASK_NAME_KEY]}" for i, task in enumerate(task_list)])
    priority_descriptions = "\n".join([f"- {k}: {v}" for k, v in priorities.items()])

    # Use f-strings to format the prompt string
    prompt = f"""
You are a prioritization agent. Your objective is to prioritize the following tasks, based on the main objective and the priorities provided.
Objective: {objective}
Tasks:
{task_descriptions}
Priorities:
{priority_descriptions}
Rank the tasks from most important to least important. Return your response in the following format:
{"".join([f"\n{i+1}. " + "{" + f"{task[TASK_NAME_KEY]}" + "}" for i, task in enumerate(task_list)])}
"""

    # Call openai API to get response
    response = openai_call(prompt, max_tokens=2000)

    # Use list comprehension and one liner to parse output
    prioritized_task_list = [{TASK_NAME_KEY: task.strip().split('. ')[1]} for task in response.strip().split('\n')]

    return prioritized_task_list