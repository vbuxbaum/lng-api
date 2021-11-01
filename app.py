import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

from feedbacks import Feedbacks

import slack
from slackeventsapi import SlackEventAdapter

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


BUX_USER_ID = "U01JGS5RE1M"
TEST_CHANNEL = "C029JE2720M"
TESTER_USER_IDS = os.environ["TESTER_USER_IDS"].split(",")


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
if (flask_env := os.environ["FLASK_ENV"]) != "production":
    client.chat_postMessage(
        channel=BUX_USER_ID,
        text=f":rocket: Iniciando em ambiente <{flask_env}>...",
    )

feedbacks_handler = Feedbacks()


@app.route("/slack/update_feedbacks", methods=["POST"])
def hello_world():
    try:
        feedbacks_handler.update_feedbacks()
    except Exception as e:
        return (
            "Ops, aconteceu isso ao tentar atualizar"
            f" os feedbacks com o anti-glossário: {e}"
        )
    return (
        ":tada: Feedbacks atualizados com o anti-glossário!"
        "\n\n"
        ":relaxed: Aguarde um momento até a novidade estabilizar"
    )


@slack_event_adapter.on("message")
def listen_messages(payload):
    event = payload.get("event", {})

    user_id = event.get("user")
    if user_id not in TESTER_USER_IDS:
        return

    text_message: str = event["text"]

    found_expression = feedbacks_handler.find_avoided_expression(text_message)

    if not found_expression:
        return

    feedback_text = feedbacks_handler.build_feedback(found_expression, user_id)
    client.chat_postMessage(channel=user_id, text=feedback_text)


if __name__ == "__main__":

    app.run(debug=True, port=3000)
