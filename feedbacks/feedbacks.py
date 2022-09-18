import json
from feedbacks.text_analyzer import TextAnalyzer
from pydantic import BaseModel


class LNGReport(BaseModel):
    used_expression: str = ""
    expression_alternatives: list = []


class Feedbacks:
    FEEDBACKS_PATH = "feedbacks.json"

    def __init__(self) -> None:
        self.load_feedbacks()

    def load_feedbacks(self) -> None:
        print("Loading feedbacks...")
        full_dict = self._read_feedbacks_base()

        self.__feedbacks = full_dict["feedbacks"]
        self.__alternatives = full_dict["alternatives"]

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

        result = []
        for avoided_expression, feedback_pattern in self.__feedbacks.items():
            found_expression = analyzer.check_for_avoided_expression(
                avoided_expression
            )

            if found_expression:

                result.append(
                    LNGReport(
                        used_expression=found_expression,
                        expression_alternatives=self.__alternatives[
                            feedback_pattern
                        ],
                    )
                )

        return result
