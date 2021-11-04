import json


class Feedbacks:
    def __init__(self):
        self.__feedbacks = {}
        self.update_feedbacks()

    def get_avoided_expressions(self) -> list:
        return list(self.__feedbacks.keys())

    def update_feedbacks(self) -> None:
        try:
            with open("data/feedbacks.json") as feedbacks_file:
                feedbacks_raw = feedbacks_file.read()
                self.__feedbacks = json.loads(feedbacks_raw)
        except FileNotFoundError:
            raise FileNotFoundError("Base de feedbacks não encontrada")
        except json.decoder.JSONDecodeError as e:
            raise SyntaxError(
                f"Base de feedbacks com sintaxe inválida : {e.args[0]}"
            )

    def find_avoided_expression(self, text_message: str) -> str:

        clean_message = "".join(
            c.lower() for c in text_message if c.isalnum() or c == " "
        )

        for avoided_expression in self.get_avoided_expressions():
            if avoided_expression.lower() in clean_message:
                return avoided_expression.lower()

        return None

    def build_feedback(self, found_word: str, user_id: str) -> str:
        intro = (
            f"Olá <@{user_id}> :green_heart:!"
            + f"Escutei você falando *{found_word}*"
        )

        explanation = f":eyes: Olha só: {self.__feedbacks[found_word]}"

        goodbye = "#VQV"

        return "\n\n".join([intro, explanation, goodbye])


if __name__ == "__main__":
    feedback_instance = Feedbacks()
    feedback_instance.get_feedbacks()
