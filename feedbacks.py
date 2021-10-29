import requests


class Feedbacks:
    def __init__(self):
        self.feedbacks = self.get_feedbacks()

    def get_feedbacks(self) -> str:
        raw_repo_base_url = (
            "https://raw.githubusercontent.com/vbuxbaum/language-feedbacks"
        )
        raw_dict = requests.get(raw_repo_base_url + "/main/feedbacks.json")

        return raw_dict.json()

    def build_feedback(self, caution_word: str, user_id: str) -> str:
        intro = f"Olá <@{user_id}>!"

        explanation = f"Escutei você falando *{caution_word}*"

        goodbye = "#VQV"

        return "\n".join([intro, explanation, goodbye])


if __name__ == "__main__":
    feedback_instance = Feedbacks()
    feedback_instance.get_feedbacks()
