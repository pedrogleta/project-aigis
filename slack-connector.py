import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from services import talk_to_agent
from aigis.tools import create_ticket

# import logging
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(level=logging.INFO)


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html


@app.event("message")
def handle_message_events(body, say, logger):
    print('mensagem: ', body['event']['text'])
    message = body['event']['text']

    agent_response = talk_to_agent(message)

    print('agent response:')
    print(agent_response)

    if agent_response == 'IGNORED':
        return

    owner = json.loads(agent_response)['owner']

    say(
        blocks=[
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": f"Gostaria de criar uma tarefa para o funcionário {owner}?"
                }
            },
            {
                "type": "actions",
                "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Sim",
                                "emoji": True
                            },
                            "style": "primary",
                            "action_id": "create_task",
                            "value": agent_response
                        },
                    {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Não",
                                "emoji": True
                            },
                            "style": "danger",
                            "action_id": "stop"
                    }
                ]
            }
        ],
        text=f"oiiii"
    )


@app.action("create_task")
def handle_create_task(ack, body, say):
    ack()

    print(body['actions'][0]['value'])
    data = json.loads(body['actions'][0]['value'])

    create_ticket(summary=data['summary'],
                  description=data['description'], name=data['owner'])

    say(
        blocks=[
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                    "text": "Tarefa criada com sucesso!"
                }
            }
        ],
        text=f"oiiii"
    )


@app.action("create_calendar_event")
def handle_create_event(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                    "text": "Adicionado ao calendário!"
                }
            }
        ],
        text=f"oiiii"
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
