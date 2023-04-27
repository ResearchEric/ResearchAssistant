import os
import openai
import time
from typing import Dict, List
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve the keys and credentials from the .env file
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Define the OpenAI API call function
def openai_call(prompt, engine="davinci", max_tokens=128, temperature=0.5):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0].text.strip()

# Define the task creation agent function
def task_creation_agent(
    objective: str, result: Dict, task_description: str, task_list: List[str]
):
    prompt = f"""
    You are a task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective},
    The last completed task has the result: {result}.
    This result was based on this task description: {task_description}. These are incomplete tasks: {', '.join(task_list)}.
    Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks.
    Return the tasks as an array."""
    response = openai_call(prompt)
    new_tasks = response.split("\n") if "\n" in response else [response]
    return [{"task_name": task_name} for task_name in new_tasks]

# Define the prioritization agent function
def prioritization_agent(task_names: List[str], objective: str):
    next_task_id = len(task_names) + 1
    prompt = f"""
    You are a task prioritization AI tasked with cleaning the formatting of and re-prioritizing the following tasks: {task_names}.
    Consider the ultimate objective of your team: {objective}.
    Do not remove any tasks. Return the result as a numbered list, like:
    #. First task
    #. Second task
    Start the task list with number {next_task_id}."""
    response = openai_call(prompt)
    new_tasks = response.split("\n") if "\n" in response else [response]
    new_tasks_list = []
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            new_tasks_list.append({"task_id": task_id, "task_name": task_name})
    return new_tasks_list

# Define the execution agent function
def execution_agent(objective: str, task: str) -> str:
    context = context_agent(query=objective, top_results_num=5)
    prompt = f"""
    You are an AI who performs one task based on the following objective: {objective}\n.
    Take into account these previously completed tasks: {context}\n.
    Your task: {task}\nResponse:"""
    return openai_call(prompt, max_tokens=2000)

# Define the context agent function
def context_agent(query: str, top_results_num: int):
    results = results_storage.query(query=query, top_results_num)
    return results

# Define your tasks storage, results storage, and other configurations here
# For example, using in-memory storage (make sure to replace it with proper storage):
tasks_storage = InMemoryTaskStorage()
results_storage = InMemoryResultsStorage()

OBJECTIVE = "Your objective here"
INITIAL_TASK = "Your initial task here"
JOIN_EXISTING_OBJECTIVE = False

# Add the initial task if starting a new objective
if not JOIN_EXISTING_OBJECTIVE:
    initial_task = {
        "task_id": tasks_storage.next_task_id(),
        "task_name": INITIAL_TASK,
    }
    tasks_storage.append(initial_task)

# Main loop
while True:
    # Get the next task from the task storage
    next_task = tasks_storage.get_next_task()

    # If there's a task, execute it and store the result
    if next_task:
        task_name = next_task["task_name"]
        print(f"Executing task: {task_name}")
        result = execution_agent(objective=OBJECTIVE, task=task_name)
        print(f"Task result: {result}")
        results_storage.store_result(task_name, result)

        # Remove the completed task from the task storage
        tasks_storage.remove_task(next_task["task_id"])

        # Create new tasks based on the result and add them to the task storage
        new_tasks = task_creation_agent(
            objective=OBJECTIVE,
            result=result,
            task_description=task_name,
            task_list=tasks_storage.get_task_names(),
        )
        tasks_storage.append_multiple(new_tasks)
    else:
        print("No more tasks to execute.")
        break

    # Get user feedback and decide if we need to prioritize tasks
    user_feedback = get_user_feedback()
    if user_feedback.lower() == "prioritize":
        print("Re-prioritizing tasks...")
        new_prioritized_tasks = prioritization_agent(
            task_names=tasks_storage.get_task_names(),
            objective=OBJECTIVE,
        )
        tasks_storage.replace(new_prioritized_tasks)

    # You can add a delay here if you want the loop to run slower
    # time.sleep(1)
