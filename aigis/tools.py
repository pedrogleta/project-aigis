import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
from difflib import SequenceMatcher


load_dotenv()

JIRA_URL = os.getenv("JIRA_URL") or ''
JIRA_EMAIL = os.getenv("JIRA_EMAIL") or ''
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN") or ''
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY") or ''


BASE_URL = f"{JIRA_URL}/rest/api/3"

# Authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


ALL_TEAM_MEMBER_NAMES = ["Pedro Leta", "Marcelo Gabriel"]


def find_team_member_by_name(name: str):
    most_likely = ''
    most_likely_ratio = 0
    for full_name in ALL_TEAM_MEMBER_NAMES:
        if SequenceMatcher(None, name, full_name).ratio() > most_likely_ratio:
            most_likely = full_name
            most_likely_ratio = SequenceMatcher(
                None, name, full_name).ratio()
    return most_likely


def find_id_by_name(name: str):
    team_member = find_team_member_by_name(name)
    if team_member == 'Pedro Leta':
        return "5ee7be561b849f0ac0904590"
    if team_member == 'Marcelo Gabriel':
        return "600f653065f20b0070ab2def"
    return ''


def create_ticket(summary: str, description: str, name: str):
    """
    Creates a new ticket in the specified Jira project.

    Args:
        name (str): The name of the person that will do the task.
        summary (str): The title of the task.
        description (str): The description of the task.

    Returns:
        str: A JSON string with the status of the call and an error_message if the call failed

    Example:
        >>> create_ticket(summary='Add CSV Import Support', description='Add support for users to import leads via csv in the Dashboard. The csv file should be parsed and validated.')
        '{"status": "success"}'
    """
    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            },
            "assignee": {
                "id": find_id_by_name(name)
            }
        }
    }

    response = requests.post(
        f"{BASE_URL}/issue",
        data=json.dumps(payload),
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        print(f"Ticket created: {response.json()['key']}")
        print(response.json())
        result = {
            "status": "success"
        }
        return str(result)
    else:
        print(
            f"Failed to create ticket: {response.status_code} - {response.text}")
        result = {
            "status": "failed",
            "error_message": response.text
        }
        return str(result)


def update_ticket(issue_key, summary=None, description=None):
    """
    Update an existing ticket.
    """
    payload = {
        "fields": {}
    }
    if summary:
        payload["fields"]["summary"] = summary
    if description:
        payload["fields"]["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": description
                        }
                    ]
                }
            ]
        }

    response = requests.put(
        f"{BASE_URL}/issue/{issue_key}",
        data=json.dumps(payload),
        headers=headers,
        auth=auth
    )

    if response.status_code == 204:
        print(f"Ticket {issue_key} updated successfully")
        return True
    else:
        print(
            f"Failed to update ticket: {response.status_code} - {response.text}")
        return False


def delete_ticket(issue_key):
    """
    Delete a ticket by its issue key.
    """
    response = requests.delete(
        f"{BASE_URL}/issue/{issue_key}",
        headers=headers,
        auth=auth
    )

    if response.status_code == 204:
        print(f"Ticket {issue_key} deleted successfully")
        return True
    else:
        print(
            f"Failed to delete ticket: {response.status_code} - {response.text}")
        return False


# Example usage
if __name__ == "__main__":
    # Create a ticket
    ticket = create_ticket(
        summary="Sample Task",
        description="This is a sample task created via API.",
        name="Pedro Leta"
    )

    # if ticket:
    #     issue_key = ticket["key"]

    #     # Update the ticket
    #     update_ticket(
    #         issue_key=issue_key,
    #         summary="Updated Sample Task",
    #         description="This ticket has been updated via API."
    #     )
