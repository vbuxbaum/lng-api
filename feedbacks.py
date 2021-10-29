import requests


class Feedbacks:
    REPO_BASE_URL = (
        "https://raw.githubusercontent.com/vbuxbaum/language-feedbacks/main"
    )

    def __init__(self):
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
