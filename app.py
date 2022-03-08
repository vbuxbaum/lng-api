from flask import Flask
import slack_sdk
from slackeventsapi import SlackEventAdapter

from feedbacks.feedbacks import Feedbacks
from app_utils.alerts import alert_dev_when_up
from app_utils.configs import (
    SLACK_SIGNING_SECRET,
    RESTRICT_CHANNELS,
    TESTER_USER_IDS,
    SLACK_BOT_TOKEN,
)


app = Flask(__name__)
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

alert_dev_when_up(slack_client, app)


feedbacks_handler = Feedbacks()
slack_event_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)


@slack_event_adapter.on("message")
def listen_messages(payload):
    message_event = payload.get("event", {})

    if not should_send_feedback(message_event):
        return

    found_expression_and_pattern = feedbacks_handler.find_avoided_expression(
        message_event.get("text")
    )

    if not found_expression_and_pattern:
        return

    feedback_text = feedbacks_handler.build_feedback(
        found_expression=found_expression_and_pattern[0],
        feedback_pattern=found_expression_and_pattern[1],
        user_id=message_event.get("user"),
        thread_link=get_permalink(message_event),
    )

    send_ephemeral_msg(message_event, feedback_text)


def send_ephemeral_msg(message_event, feedback_text):
    try:
        slack_client.chat_postEphemeral(
            channel=message_event.get("channel"),
            thread_ts=message_event.get("thread_ts"),
            user=message_event.get("user"),
            text=feedback_text,
        )
    except slack_sdk.errors.SlackApiError as e:
        if e.response["error"] == "not_in_channel":
            slack_client.conversations_join(
                channel=message_event.get("channel")
            )
            send_ephemeral_msg(message_event, feedback_text)


def get_permalink(message_event):
    return slack_client.chat_getPermalink(
        channel=message_event.get("channel"),
        message_ts=message_event.get("ts"),
    )["permalink"]


def should_send_feedback(message_event):
    return (
        message_event.get("channel") not in RESTRICT_CHANNELS
        # REMOVER CONDIÇÃO ABAIXO no dia do lançamento oficial
        and message_event.get("user") in TESTER_USER_IDS
    )


@app.route("/health")
def health():
    return "Ok"


if __name__ == "__main__":

    app.run(debug=True, port=3000)
