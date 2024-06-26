import json
import glob
import os
import sys


def load_logs(file_path):
    with open(file_path, "r") as file:
        return json.load(file)  # Load the entire JSON file containing all issues


def load_logs_from_dir(directory_path):
    issues = {}
    # Assuming all log files follow the pattern 'agent_logs*.json'
    for file_path in glob.glob(os.path.join(directory_path, 'agent_logs.json06_20_*')):
        with open(file_path, 'r') as file:
            logs = json.load(file)
            issue_id = list(logs.keys())[0]
            if issue_id in issues:
                print("!!!!! duplicate issue-id entry found !!!!!")
            issues[issue_id] = logs[issue_id]
    return issues


def extract_details(agent_logs):
    data = []
    for log in agent_logs:
        # from pprint import pprint
        # pprint(log)
        if log["agent_action"] == "agent_finish":
            agent_action = "agent_finish"
            agent_output = log["agent_output"]
        else:
            agent_action = json.loads(log["agent_action"])
            tool_name = agent_action.get("tool", "N/A")
            tool_input = agent_action.get("tool_input", "N/A")
            tool_output = log.get("tool_output", "N/A")
            agent_thought = agent_action.get("log", "No thoughts recorded")

        data.append(
            {
                "tool_name": tool_name or agent_action,
                "tool_input": tool_input,
                "tool_output": tool_output or agent_output,
                "agent_thought": agent_thought,
            }
        )
    return data


def generate_html_1(issues_data, output_file):
    html_content = """
    <html>
    <head>
        <title>Agent Action Report by Issue</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #dddddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Agent Action Report by Issue</h1>
    """
    for issue, data in issues_data.items():
        html_content += f"<h2>{issue}</h2>"
        html_content += """
        <table>
            <tr>
                <th>Tool Name</th>
                <th>Tool Input</th>
                <th>Tool Output</th>
                <th>Agent Thought</th>
            </tr>
        """
        for entry in data:
            html_content += f"""
                <tr>
                    <td>{entry['tool_name']}</td>
                    <td>{entry['tool_input']}</td>
                    <td>{entry['tool_output']}</td>
                    <td>{entry['agent_thought']}</td>
                </tr>
            """
        html_content += "</table>"
    html_content += """
    </body>
    </html>
    """

    with open(output_file, "w") as file:
        file.write(html_content)
    print(f"HTML report generated: {output_file}")


def generate_html1(issues_data, output_file):
    html_content = """
    <html>
    <head>
        <title>Agent Action Report by Issue</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .collapsible {
                background-color: #777;
                color: white;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 15px;
            }
            .active, .collapsible:hover {
                background-color: #555;
            }
            .content, .tool-output-content {
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f1f1f1;
            }
        </style>
    </head>
    <body>
        <h1>Agent Action Report by Issue</h1>
    """
    for issue_idx, (issue, data) in enumerate(issues_data.items()):
        html_content += f"""
        <button class="collapsible">Issue {issue}</button>
        <div class="content">
            <table>
                <tr>
                    <th>Tool Name</th>
                    <th>Tool Input</th>
                    <th>Tool Output</th>
                    <th>Agent Thought</th>
                </tr>
        """
        for entry_idx, entry in enumerate(data):
            tool_output_id = f"tool-output-content-{issue_idx}-{entry_idx}"
            html_content += f"""
                <tr>
                    <td>{entry['tool_name']}</td>
                    <td>{entry['tool_input']}</td>
                    <td>
                        <button class="collapsible">View Output</button>
                        <div id="{tool_output_id}" class="tool-output-content">{entry['tool_output']}</div>
                    </td>
                    <td>{entry['agent_thought']}</td>
                </tr>
            """
        html_content += "</table></div>"

    html_content += """
    <script>
        var coll = document.getElementsByClassName("collapsible");
        for (var i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        }
    </script>
    </body>
    </html>
    """

    with open(output_file, "w") as file:
        file.write(html_content)
    print(f"HTML report generated: {output_file}")


def format_thought(thought):
    # print(thought)
    # Initial setup for default values if any of the parts are missing
    action = "No action specified"
    action_input = "No input provided"
    thought_text = "No thoughts recorded"

    # Extracting "Action"
    if "Action: " in thought:
        action_start = thought.find("Action:") + len("Action:")
        action_end = thought.find("Action Input:")
        action = thought[action_start:action_end].strip()

    # Extracting "Action Input"
    if "Action Input: " in thought:
        input_start = thought.find("Action Input:") + len("Action Input:")
        input_end = thought.find("Thought:")
        action_input = thought[input_start:].strip()

    # Extracting "Thought"
    if "Thought: " in thought:
        thought_start = thought.find("Thought:") + len("Thought:")
        thought_end = thought.find("Action: ")
        thought_text = thought[thought_start:thought_end].strip()

    return f'<div class="action">Action: {action}</div><div class="action-input">Action Input: {action_input}</div><div class="thought">Thought: {thought_text}</div>'


def generate_html(issues_data, output_file):
    html_content = """
    <html>
    <head>
        <title>Agent Action Report by Issue</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #dddddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .collapsible { cursor: pointer; color: blue; text-decoration: underline; }
            .content { display: none; padding: 4px; }
            .action { font-weight: bold; color: green; }
            .action-input { font-weight: bold; color: darkorange; }
            .thought { color: darkblue; }
        </style>
        <script>
            function toggleVisibility(id) {
                var x = document.getElementById(id);
                if (x.style.display === "none") {
                    x.style.display = "block";
                } else {
                    x.style.display = "none";
                }
            }
        </script>
    </head>
    <body>
        <h1>Agent Action Report by Issue</h1>
    """
    for issue_idx, (issue, data) in enumerate(issues_data.items()):
        html_content += f"<h2>{issue}</h2><table><tr><th>Tool Name</th><th>Tool Input</th><th>Tool Output</th><th>Agent Thought</th></tr>"
        for entry_idx, entry in enumerate(data):
            content_id = f"content-{issue_idx}-{entry_idx}"
            short_output = (
                (entry["tool_output"][:75] + "...")
                if len(entry["tool_output"]) > 78
                else entry["tool_output"]
            )
            formatted_thought = format_thought(entry["agent_thought"])
            html_content += f'<tr><td>{entry["tool_name"]}</td><td>{entry["tool_input"]}</td><td><span class="collapsible" onclick="toggleVisibility(\'{content_id}\')">{short_output}</span><div id="{content_id}" class="content">{entry["tool_output"]}</div></td><td>{formatted_thought}</td></tr>'
        html_content += "</table>"
    html_content += "</body></html>"

    with open(output_file, "w") as file:
        file.write(html_content)
    print(f"HTML report generated: {output_file}")


def main(log_file_dir, output_html_file):
    issues = load_logs_from_dir(log_file_dir)
    issues_data = {issue: extract_details(logs) for issue, logs in issues.items()}
    generate_html1(issues_data, output_html_file)


if __name__ == "__main__":
    log_file_path = sys.argv[1]
    output_html_file = "agent_action_report_by_issue.html"  # Desired output HTML file
    main(log_file_path, output_html_file)
