from slack_sdk.errors import SlackApiError
from app_utils.configs import (
    DEV_USER_ID,
    FLASK_ENV,
)


def alert_dev_when_up(client, app):
    if not DEV_USER_ID:
        return

    try:
        client.chat_postMessage(
            channel=DEV_USER_ID,
            text=f":rocket: Iniciando em ambiente <{FLASK_ENV}>...",
        )
    except SlackApiError:
        app.logger.debug(
            f"Failed to alert following DEV_USER_ID: {DEV_USER_ID}"
        )
