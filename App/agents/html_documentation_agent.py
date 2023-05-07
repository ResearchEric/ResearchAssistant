from typing import Dict, List


def html_documentation_agent(objective: str, context: Dict, task_list: List[Dict[str, str]]) -> str:
    # Create HTML header
    html = "<html><head><title>Documentation</title></head><body>"

    # Add objective to HTML
    html += f"<h1>{objective}</h1>"

    # Add context to HTML
    html += "<h2>Context</h2>"
    html += "<ul>"
    for key, value in context.items():
        html += f"<li>{key}: {value}</li>"
    html += "</ul>"

    # Add task list to HTML
    html += "<h2>Task List</h2>"
    html += "<ul>"
    for task in task_list:
        html += f"<li>{task['task_name']}</li>"
    html += "</ul>"

    # Close HTML tags
    html += "</body></html>"

    return html
