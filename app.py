import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

from feedbacks import Feedbacks

import slack
from slackeventsapi import SlackEventAdapter


RONA_USER_ID = "U023CHB5UR0"
BUX_USER_ID = "U01JGS5RE1M"

TESTER_USER_IDS = {RONA_USER_ID, BUX_USER_ID}
TEST_CHANNEL = "C029JE2720M"

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app
)

client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
client.chat_postMessage(channel=BUX_USER_ID, text="... iniciando ...")

feedbacks_handler = Feedbacks()


@app.route("/slack/update_feedbacks", methods=["POST"])
def hello_world():
    try:
        feedbacks_handler.update_feedbacks()
    except Exception as e:
        return (
            "Ops, aconteceu isso ao tentar atualizar"
            f" os feedbacks com o repositório principal: {e}"
        )
    return (
        "Feedbacks atualizados com o repositório principal! :tada:"
        "\n\n"
        "Aguarde um momento até a novidade estabilizar :relaxed:"
    )


@slack_event_adapter.on("message")
def listen_messages(payload):
    event = payload.get("event", {})

    user_id = event.get("user")
    if user_id not in TESTER_USER_IDS:
        print(event.get("text", "None"))
        return

    text_message: str = event["text"]
    caution_words = feedbacks_handler.get_caution_words()

    oopsie_words = [
        word.lower()
        for word in text_message.split(" ")
        if word.lower() in caution_words
    ]

    if not oopsie_words:
        return

    feedback_text = feedbacks_handler.build_feedback(oopsie_words[0], user_id)
    client.chat_postMessage(channel=user_id, text=feedback_text)


if __name__ == "__main__":

    app.run(debug=True, port=3000)
