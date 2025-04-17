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
    print('got in the event specific handler')

    print(body['event']['text'])
    message = body['event']['text']

    if 'hello' in message:
        say(f"Hey there <@{body['event']['user']}>!")


# @app.message("hello")
# def message_hello(message, say):
#     print('got in this handler')
#     print(message)
#     # say() sends a message to the channel where the event was triggered

#     say(f"Hey there <@{message['user']}>!")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
