import re
from typing import Dict, List

from openai_call import openai_call


def html_documentation_agent(
    objective: str, context: str, task_list: List[Dict[str, str]]
) -> str:

    task_descriptions = "\n".join(
        [f"{i+1}. {task['task_name']}" for i, task in enumerate(task_list)])

    prompt = f"""
You are an html documentation agent. Your objective is to create a well-structured document based on the main objective, the current context, and the list of tasks provided. The document should guide the user through the project and help them understand the process.

Objective: {objective}
Context: {context}
Tasks:
{task_descriptions}

Generate a well-structured html document that outlines the project, explaining the context and guiding the user through the tasks in a clear and understandable manner.
    """

    print(
        f'\n************ HTML DOCUMENTATION AGENT PROMPT ************\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(
        f'\n*********** HTML DOCUMENTATION AGENT RESPONSE ***********\n{response}\n')

    return response.strip()
