import json


class Feedbacks:
    DATA_PATH = "data/"
    FEEDBACKS_PATH = DATA_PATH + "feedbacks.json"

    def __init__(self):
        self._load_feedbacks()

    def _get_avoided_expressions(self) -> list:
        return list(self.__feedbacks.keys())

    def _load_feedbacks(self) -> None:
        print("loading feedbacks...")
        try:
            with open(self.FEEDBACKS_PATH) as feedbacks_file:
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
            char.lower()
            for char in text_message
            if char.isalnum() or char == " "
        )

        for avoided_expression in self._get_avoided_expressions():
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
        feedback_path = self.DATA_PATH + self.__feedbacks[found_word]

        with open(feedback_path) as feedback_file:
            feedback_text = feedback_file.read()

        return self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]
