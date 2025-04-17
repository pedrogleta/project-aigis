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

    if 'hello' in message:
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Hey there <@{body['event']['user']}>!"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click Me"},
                        "action_id": "button_click"
                    }
                }
            ],
            text=f"Hey there <@{body['event']['user']}>!"
        )


@app.action("button_click")
def handle_button_click(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Button clicked by <@{body['user']['id']}>!"}
            }
        ],
        text=f"Button clicked by <@{body['user']['id']}>!"
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
