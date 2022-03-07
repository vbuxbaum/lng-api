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

        analyzer = TextAnalyzer(text_message)

        for avoided_expression, feedback_pattern in self.__feedbacks.items():
            found_expression = analyzer.check_for_avoided_expression(
                avoided_expression
            )

            if found_expression:
                return found_expression, feedback_pattern

        return None

    def build_feedback(
        self,
        found_expression: str,
        feedback_pattern: str,
        user_id: str,
        thread_link: str,
    ) -> str:
        return "\n\n".join(
            [
                self._build_intro(found_expression, user_id, thread_link),
                self._build_explanation(feedback_pattern),
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

    def _build_explanation(self, found_pattern: str) -> str:

        feedback_text = self.__explanations[found_pattern]

        return self.__default_text["explanation"].replace(
            "<feedback>", feedback_text
        )

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]
