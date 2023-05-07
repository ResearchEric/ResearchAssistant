import re
from typing import Dict

from openai_call import openai_call


def execution_agent(task: Dict[str, str]) -> Dict[str, str]:
    task_description = task["task_name"]
    prompt = generate_prompt(task_description)

    print(
        f'\n*************** EXECUTION AGENT PROMPT ***************\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(
        f'\n************** EXECUTION AGENT RESPONSE **************\n{response}\n')

    data = clean_response(response)

    return {"task_name": task_description, "data": data}


def generate_prompt(task_description: str) -> str:
    return f"""
You are an execution agent given the following task: {task_description}
Carry out the task and provide a detailed report on the process and results."""


def clean_response(response: str) -> str:
    return re.sub(r'[^\w\s_.,:;?!-]+', '', response).strip()
