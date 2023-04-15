import json
from src.feedback.text_analyzer import TextAnalyzer
from src.data_model import AnalyzerOptions, LNGReport
from pathlib import Path


class Feedbacks:
    def __init__(self, analyzer_options=None) -> None:
        self.FEEDBACKS_PATH = (
            Path(__file__).parent / "../../app_data/feedbacks.json"
        )

        self.load_options(analyzer_options)

    @property
    def options(self):
        return self.__options

    def load_options(self, analyzer_options) -> None:
        print("Loading feedbacks...")

        if analyzer_options is None:
            self.__options = AnalyzerOptions(**self._read_feedbacks_base())
        else:
            self.__options = analyzer_options

        print("Feedbacks loaded!")

    def _read_feedbacks_base(self) -> dict:

        try:
            with open(self.FEEDBACKS_PATH) as feedbacks_file:
                return json.load(feedbacks_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Base de feedbacks não encontrada : {e}")
        except json.decoder.JSONDecodeError as e:
            raise SyntaxError(
                f"Base de feedbacks com sintaxe inválida : {e.args[0]}"
            )

    def find_avoided_expression(self, text_message: str) -> list[LNGReport]:

        analyzer = TextAnalyzer(text_message)

        result = []
        for (
            avoided_expression,
            feedback_pattern,
        ) in self.options.feedbacks.items():

            found_expression = analyzer.check_for_avoided_expression(
                avoided_expression
            )

            if not found_expression:
                continue

            alternatives = self.options.alternatives.get(feedback_pattern, [])

            report = LNGReport(
                used_expression=found_expression,
                expression_alternatives=alternatives,
            )

            result.append(report)

        return result
