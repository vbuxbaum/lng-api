import json
from feedbacks.text_analyzer import TextAnalyzer
from pydantic import BaseModel


class AnalyzerOptions(BaseModel):
    feedbacks: dict
    alternatives: dict

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "feedbacks": {
                    "os amigos": "os_amigos",
                    "os trabalhadores": "os_trabalhadores",
                },
                "alternatives": {
                    "os_amigos": ["as amizades", "as pessoas amigas"],
                    "os_trabalhadores": [
                        "quem trabalha",
                        "as pessoas trabalhadoras",
                    ],
                },
            }
        }


class LNGReport(BaseModel):
    used_expression: str
    expression_alternatives: list


class Feedbacks:
    def __init__(self, analyzer_options=None) -> None:
        self.FEEDBACKS_PATH = "feedbacks.json"
        self.load_feedbacks(analyzer_options)

    def load_feedbacks(self, analyzer_options) -> None:
        print("Loading feedbacks...")
        if analyzer_options is None:
            full_dict = self._read_feedbacks_base()
        else:
            full_dict = analyzer_options

        self.__feedbacks = full_dict["feedbacks"]
        self.__alternatives = full_dict["alternatives"]

        print("Feedbacks loaded!")

    def _read_feedbacks_base(self) -> dict:
        try:
            with open(self.FEEDBACKS_PATH) as feedbacks_file:
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

                report = LNGReport(
                    used_expression=found_expression,
                    expression_alternatives=self.__alternatives.get(
                        feedback_pattern, []
                    ),
                )

                result.append(report)

        return result
