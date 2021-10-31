import os
import requests
from pathlib import Path
from dotenv import load_dotenv


class Feedbacks:
    def __init__(self):
        env_path = Path(".") / ".env"
        load_dotenv(dotenv_path=env_path)
        self.REPO_BASE_URL = os.environ["REPO_BASE_URL"]

        self.__feedbacks = {}
        self.update_feedbacks()

    def get_caution_words(self) -> str:
        return self.__feedbacks.keys()

    def update_feedbacks(self) -> dict:
        print("Updating feedbacks from GitHub . . . . ")
        raw_dict = requests.get(self.REPO_BASE_URL + "/feedbacks.json")
        self.__feedbacks = raw_dict.json()

    def build_feedback(self, caution_word: str, user_id: str) -> str:
        intro = (
            f"Olá <@{user_id}> :green_heart:!"
            + f"Escutei você falando *{caution_word}*"
        )

        explanation = f":eyes: Olha só: {self.__feedbacks[caution_word]}"

        goodbye = "#VQV"

        return "\n\n".join([intro, explanation, goodbye])


if __name__ == "__main__":
    feedback_instance = Feedbacks()
    feedback_instance.get_feedbacks()
