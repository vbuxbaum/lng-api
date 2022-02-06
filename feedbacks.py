import json


class Feedbacks:
    FEEDBACKS_PATH = "feedbacks.json"

    def __init__(self) -> None:
        self.load_feedbacks()

    def load_feedbacks(self) -> None:
        print("Loading feedbacks...")
        full_dict = self._read_feedbacks_base()

        self.__feedbacks = full_dict["feedbacks"]
        self.__default_text = full_dict["default_text"]
        self.__explanations = full_dict["explanation_patterns"]

    @classmethod
    def _read_feedbacks_base(cls) -> dict:
        try:
            with open(cls.FEEDBACKS_PATH) as feedbacks_file:
                return json.load(feedbacks_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Base de feedbacks não encontrada : {e.args[0]}"
            )
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

    def _get_avoided_expressions(self) -> list:
        return list(self.__feedbacks.keys())

    def build_feedback(self, found_word: str, user_id: str) -> str:
        return "\n\n".join(
            [
                self._build_intro(found_word, user_id),
                self._build_explanation(found_word),
                self._build_goodbye(),
            ]
        )

    def _build_intro(self, found_word: str, user_id: str) -> str:
        return (
            self.__default_text["intro"]
            .replace("<user_id>", user_id)
            .replace("<found_word>", found_word)
        )

    def _build_explanation(self, found_word: str) -> str:
        feedback_text = self.__explanations[self.__feedbacks[found_word]]

        return self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]
