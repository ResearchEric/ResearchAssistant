README

This is an app that creates, prioritizes, executes, and documents tasks based on a given objective. The objective can be set by the user through an environment variable. The app is run through the command line.

Functionalities:

- creating tasks: tasks are created based on the context of the objective and the tasks that already exist in the task list
- prioritizing tasks: tasks are prioritized based on their importance in achieving the objective
- executing tasks: tasks are executed one by one. Each task execution is prompted with its name, followed by its execution result.
- documentation: a documentation of the app and the tasks executed is generated in an html page.

Usage:

1. Set the OBJECTIVE and INITIAL_TASK environment variables
2. Run the app using Python from the command line: python app.py
3. The app will prompt the user to choose an action:
  - Enter a number: the app will automatically process tasks for the given number of hours.
  - Enter "s": The task list will be saved to a file called task_list.txt and the app will exit.
  - Enter "e": The app will exit without saving the task list.
  - Any other input: the app will create, prioritize, execute tasks, and generate documentation.

Dependencies:

- Python 3.7 or higher
- openai
- python-dotenv

Configuration: 

The user can configure the app by setting environment variables:

- OBJECTIVE: the objective for which tasks are created, prioritized, executed, and documented.
- INITIAL_TASK: the initial task to be added to the task list.

File Structure:

- agents folder: includes modules for each agent that performs a specific functionality
- app.py: the main file that runs the app
- README.txt: a guide for the user to run the app
- .env: environment variables needed for the app to run

Note: 

The current implementation of the app is not modular, hence it could be difficult to debug. However, some refactoring options have been provided at the beginning of the code.
