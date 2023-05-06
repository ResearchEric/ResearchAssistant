import re
from typing import Dict, List

from openai_call import openai_call

def context_agent(
    objective: str, task_list: List[Dict[str, str]], context: str, subject: str
) -> Dict[str, str]:

    task_descriptions = "\n".join([f"{i+1}. {task['task_name']}" for i, task in enumerate(task_list)])

    prompt = f"""
You are a context agent. Your objective is to provide context to the following tasks, based on the main objective, the specific context, and the subject.

Objective: {objective}
Context: {context}
Subject: {subject}
Tasks:
{task_descriptions}

For each task, provide a brief explanation of how it relates to the context and subject. Return your response in the following format:

1. Task 1 - Explanation for Task 1
2. Task 2 - Explanation for Task 2
...
n. Task n - Explanation for Task n
    """

    print(f'\n*************** CONTEXT AGENT PROMPT ***************\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(f'\n************** CONTEXT AGENT RESPONSE **************\n{response}\n')

    explanations = response.split('\n')
    context_mapping = {}
    for explanation in explanations:
        explanation_parts = explanation.strip().split(" - ", 1)
        if len(explanation_parts) == 2:
            task_id = "".join(s for s in explanation_parts[0] if s.isnumeric())
            task_context = re.sub(r"[^\w\s_.,:;?!-]+", "", explanation_parts[1]).strip()
            if task_context and task_id.isnumeric():
                context_mapping[int(task_id) - 1] = task_context

    out = [{"task_name": task["task_name"], "context": context_mapping.get(i, "")} for i, task in enumerate(task_list)]

    return out
