import re
from typing import Dict, List
import os
from dotenv import load_dotenv
from agents.openai_call import openai_call


load_dotenv()


def context_agent(
    task_list: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    objective = os.getenv("OBJECTIVE")
    context = os.getenv("CONTEXT")
    subject = os.getenv("SUBJECT")

    task_descriptions = "\n".join(
        [f"{i+1}. {task['task_name']}" for i, task in enumerate(task_list)])
    prompt = generate_prompt(objective, context, subject, task_descriptions)

    print(
        f'\n*************** CONTEXT AGENT PROMPT ***************\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(
        f'\n************** CONTEXT AGENT RESPONSE **************\n{response}\n')

    context_mapping = extract_context_mapping(response)
    out = apply_context_mapping(task_list, context_mapping)

    return out


def generate_prompt(objective: str, context: str, subject: str, task_descriptions: str) -> str:
    return f"""
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


def extract_context_mapping(response: str) -> Dict[int, str]:
    explanations = response.split('\n')
    context_mapping = {}
    for explanation in explanations:
        explanation_parts = explanation.strip().split(" - ", 1)
        if len(explanation_parts) == 2:
            task_id = "".join(s for s in explanation_parts[0] if s.isnumeric())
            task_context = re.sub(r"[^\w\s_.,:;?!-]+",
                                  "", explanation_parts[1]).strip()
            if task_context and task_id.isnumeric():
                context_mapping[int(task_id) - 1] = task_context
    return context_mapping


def apply_context_mapping(task_list: List[Dict[str, str]], context_mapping: Dict[int, str]) -> List[Dict[str, str]]:
    return [{"task_name": task["task_name"], "context": context_mapping.get(i, "")} for i, task in enumerate(task_list)]
