from typing import Dict, List

PRIORITY_KEY = "priority"
TASK_NAME_KEY = "task_name"


def prioritization_agent(task_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Assign priority to each task based on its position in the list
    for i, task in enumerate(task_list):
        task[PRIORITY_KEY] = i

    # Sort tasks by priority in ascending order
    sorted_tasks = sorted(task_list, key=lambda x: x[PRIORITY_KEY])

    # Remove priority key from tasks
    for task in sorted_tasks:
        del task[PRIORITY_KEY]

    # Return sorted tasks
    return sorted_tasks
