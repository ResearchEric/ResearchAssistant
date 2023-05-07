from typing import Dict
from agents.openai_call import openai_call


def execution_agent(task_description: str, context: Dict) -> Dict:
    prompt = f"""
You are an execution agent. Your objective is to execute the task: {task_description}.
Context: {context}
What is the result of the task?
"""

    # Call openai API to get response
    response = openai_call(prompt, max_tokens=2000)

    # Use dictionary comprehension to parse output
    execution_result = {task_description: response.strip()}

    return execution_result
