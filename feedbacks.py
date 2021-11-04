import json


class Feedbacks:
    def __init__(self):
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

    def new_update_feedbacks(self) -> None:
        try:
            with open("data/feedbacks_new.json") as feedbacks_file:
                self.__feedbacks = json.load(feedbacks_file)["feedbacks"]
                self.__default_text = json.load(feedbacks_file)["default_text"]
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

    def new_build_feedback(self, found_word: str, user_id: str) -> str:
        intro = (
            self.__default_text["intro"]
            .replace("<user_id>", user_id)
            .replace("<found_word>", found_word)
        )

        with open(f"{self.__feedbacks[found_word]}.slack") as feedback_file:
            feedback_text = feedback_file.read()

        explanation = self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

        goodbye = self.__default_text["goodbye"]

        return "\n\n".join([intro, explanation, goodbye])


if __name__ == "__main__":
    feedback_instance = Feedbacks()
    feedback_instance.get_feedbacks()
