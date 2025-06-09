import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
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

    # Call AI

    # Get params for creating jira ticket

    if 'hello' in message:
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "Gostaria de criar uma tarefa para o funcionário Marcelo?"
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
                                "value": "STRINGIFIED JSON"
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

    say(
        blocks=[
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                    "text": "Tarefa criada com sucesso!"
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                    "text": "Gostaria de adicionar um envento ao calendário para conferir o progresso em uma semana?"
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
                            "action_id": "create_calendar_event"
                        },
                    {
                            "type": "button",
                            "text": {
                                    "type": "plain_text",
                                    "text": "Não",
                                    "emoji": True
                            },
                            "style": "danger",
                            "action_id": "no_action"
                        }
                ]
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
