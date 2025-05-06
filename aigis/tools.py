import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


BASE_URL = f"{JIRA_URL}/rest/api/3"

# Authentication
auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def create_ticket(summary, description, issue_type="Task"):
    """
    Create a new ticket in the specified Jira project.
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
                "name": issue_type
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
        return response.json()
    else:
        print(
            f"Failed to create ticket: {response.status_code} - {response.text}")
        return None


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
        issue_type="Task"
    )

    if ticket:
        issue_key = ticket["key"]

        # Update the ticket
        update_ticket(
            issue_key=issue_key,
            summary="Updated Sample Task",
            description="This ticket has been updated via API."
        )

        # Delete the ticket
        # delete_ticket(issue_key)
