from google.adk.agents import Agent
from .tools import create_ticket

root_agent = Agent(
    name="aigis",
    model="gemini-2.0-flash",
    description=(
        "Agent that listens to manager-employee conversations and decides whether he should create a jira task"
    ),
    instruction=(
        """
        You are an agent that listens to managers talking to employees and creates tasks when the manager asks something of the employee.
        You can use the create_ticket tool to create Jira tasks.
        ALWAYS provide name, summary and description to the tool.
        IF you detect a request being made that could become a Jira task, create a Jira task for it and respond ONLY with SUCCESS
        ELSE respond ONLY with IGNORED
        """
    ),
    tools=[create_ticket]
)
