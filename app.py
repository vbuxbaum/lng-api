import os

# from slack_bolt import App
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

from feedback_resolver import get_feedbacks, build_feedback

BUX_USER_ID = "U01JGS5RE1M"
TEST_CHANNEL = "U01JGS5RE1M"

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
client.chat_postMessage(channel=TEST_CHANNEL, text="... iniciando ...")


@slack_event_adapter.on("message")
def listen_messages(payload):
    event = payload.get("event", {})

    user_id = event["user"]
    # channel_id = event["channel"]
    text_message: str = event["text"]

    if user_id != BUX_USER_ID:
        return

    oopsie_words = [
        word
        for word in text_message.split(" ")
        if word.lower() in caution_words
    ]

    if oopsie_words:
        client.chat_postMessage(
            channel=TEST_CHANNEL, text=build_feedback(oopsie_words, user_id)
        )


if __name__ == "__main__":
    caution_words = get_feedbacks()

    app.run(debug=True, port=3000)
