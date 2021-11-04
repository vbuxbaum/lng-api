import json


class Feedbacks:
    def __init__(self):
        self.load_feedbacks()

    def get_avoided_expressions(self) -> list:
        return list(self.__feedbacks.keys())

    def load_feedbacks(self) -> None:
        try:
            with open("data/feedbacks.json") as feedbacks_file:
                full_dict = json.load(feedbacks_file)
                self.__feedbacks = full_dict["feedbacks"]
                self.__default_text = full_dict["default_text"]
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
        intro = self._build_intro(found_word, user_id)

        explanation = self._build_explanation(found_word)

        goodbye = self._build_goodbye()

        return "\n\n".join([intro, explanation, goodbye])

    def _build_intro(self, found_word: str, user_id: str) -> str:
        return (
            self.__default_text["intro"]
            .replace("<user_id>", user_id)
            .replace("<found_word>", found_word)
        )

    def _build_explanation(self, found_word: str) -> str:
        feedback_path = f"data/{self.__feedbacks[found_word]}.slack"

        with open(feedback_path) as feedback_file:
            feedback_text = feedback_file.read()

        return self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]


if __name__ == "__main__":
    feedback_instance = Feedbacks()
    feedback_instance.get_feedbacks()
