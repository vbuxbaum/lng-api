import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

from feedbacks import Feedbacks

import slack
from slackeventsapi import SlackEventAdapter

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


RESTRICT_CHANNELS = os.environ["RESTRICT_CHANNELS"].split(",")
TESTER_USER_IDS = os.environ["TESTER_USER_IDS"].split(",")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])

if (flask_env := os.environ["FLASK_ENV"]) != "production":
    DEV_USER_ID = os.environ["DEV_USER_ID"]
    client.chat_postMessage(
        channel=DEV_USER_ID,
        text=f":rocket: Iniciando em ambiente <{flask_env}>...",
    )

feedbacks_handler = Feedbacks()


@slack_event_adapter.on("message")
def listen_messages(payload):
    event = payload.get("event", {})

    user_id = event.get("user")
    if (
        event.get("channel") in RESTRICT_CHANNELS
        # REMOVER CONDIÇÃO ABAIXO no dia do lançamento oficial
        or user_id not in TESTER_USER_IDS
    ):
        return

    text_message: str = event["text"]

    found_expression = feedbacks_handler.find_avoided_expression(text_message)

    if not found_expression:
        return

    feedback_text = feedbacks_handler.build_feedback(found_expression, user_id)
    client.chat_postMessage(channel=user_id, text=feedback_text)


if __name__ == "__main__":

    app.run(debug=True, port=3000)
