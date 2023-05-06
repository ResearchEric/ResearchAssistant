from typing import Dict, List
from openai_call import openai_call


def task_creation_agent(
        objective: str, result: Dict, task_description: str, task_list: List[str],
        max_tasks: int = 10, remove_duplicates: bool = True
) -> List[Dict[str, str]]:

    prompt_description = f"Create a list of new tasks in order to meet the objective: {objective}.\n"
    if task_list:
        prompt_description += f"The last completed task has the result:\n{result['data']}\\n"
        prompt_description += f"Based on the result, create a list of new tasks that do not overlap with the following incomplete tasks:\n"
        prompt_description += "\n".join(task_list) + "\n"
    else:
        prompt_description += f"The last completed task was based on this task description:\n{task_description}\n"

    prompt = f"""
{prompt_description}
Return the top {max_tasks} unique new tasks that meet the objective, with one task per line in your response. 
The result must be a numbered list in the format:
    
#. First task
#. Second task
        
The number of each entry must be followed by a period.
Do not include any headers before your numbered list. Do not follow your numbered list with any other output."""

    print(
        f'\n************** TASK CREATION AGENT PROMPT *************\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(
        f'\n************* TASK CREATION AGENT RESPONSE ************\n{response}\n')

    # Process response into a list of tasks
    new_tasks = []
    for task_string in response.split('\n'):
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_name = re.sub(r'[^\w\s_]+', '', task_parts[1]).strip()
            if task_name.strip():
                new_tasks.append(task_name)

    # Remove duplicates
    if remove_duplicates:
        new_tasks = list(set(new_tasks))

    # Limit to max_tasks
    new_tasks = new_tasks[:max_tasks]

    # Format results
    out = [{"task_name": task_name} for task_name in new_tasks]
    return out
