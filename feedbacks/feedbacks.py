import json

from feedbacks.text_analyzer import TextAnalyzer


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

        print("Feedbacks loaded!")

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

        clean_message = self.clear_message(text_message)
        analyzer = TextAnalyzer(clean_message)

        for avoided_expression in self._get_avoided_expressions():
            if avoided_expression in clean_message:
                return (
                    avoided_expression
                    if avoided_expression.count(" ") != 1
                    else analyzer.check_gender_neutrality(avoided_expression)
                )

        return None

    def clear_message(self, text_message):
        try:
            clean_message = "".join(
                char
                for char in text_message.lower()
                if char.isalnum() or char == " "
            )
        except AttributeError:
            raise TypeError(
                f"Argument needs to be a string, not {type(text_message)}"
            )

        return clean_message

    def _get_avoided_expressions(self) -> list:
        return list(self.__feedbacks.keys())

    def build_feedback(
        self, found_word: str, user_id: str, thread_link: str
    ) -> str:
        return "\n\n".join(
            [
                self._build_intro(found_word, user_id, thread_link),
                self._build_explanation(found_word),
                self._build_goodbye(),
            ]
        )

    def _build_intro(
        self, found_word: str, user_id: str, thread_link: str
    ) -> str:
        return (
            self.__default_text["intro"]
            .replace("<user_id>", user_id)
            .replace("<found_word>", found_word)
            .replace("<thread_link>", thread_link)
        )

    def _build_explanation(self, found_word: str) -> str:
        found_pattern = min(
            pattern
            for pattern in self.__feedbacks
            if pattern in found_word
        )

        feedback_text = self.__explanations[self.__feedbacks[found_pattern]]

        return self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]
