import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

FLASK_ENV = os.environ["FLASK_ENV"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
RESTRICT_CHANNELS = os.environ["RESTRICT_CHANNELS"].split(";")
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

TESTER_USER_IDS = os.environ.get("TESTER_USER_IDS").split(";")
DEV_USER_ID = os.environ.get("DEV_USER_ID")
