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

        result = []
        for avoided_expression, feedback_pattern in self.__feedbacks.items():
            found_expression = analyzer.check_for_avoided_expression(
                avoided_expression
            )

            if found_expression:
                result.append((found_expression, feedback_pattern))

        return result

    def build_feedback(
        self,
        expression_and_pattern: list,
        user_id: str,
        thread_link: str,
    ) -> str:
        expressions = [expression for expression, _ in expression_and_pattern]
        patterns = [pattern for _, pattern in expression_and_pattern]

        return "\n\n".join(
            [
                self._build_intro(expressions, user_id, thread_link),
                self._build_explanation(patterns),
                self._build_goodbye(),
            ]
        )

    def _build_intro(
        self, found_expressions: str, user_id: str, thread_link: str
    ) -> str:

        expressions_to_mention = self.__expressions_to_mention(
            found_expressions
        )

        return (
            self.__default_text["intro"]
            .replace("<user_id>", user_id)
            .replace("<found_expressions>", expressions_to_mention)
            .replace("<thread_link>", thread_link)
        )

    def __expressions_to_mention(self, expressions):
        expressions_to_mention = f'"*{expressions[0]}*"'

        if len(expressions) == 1:
            return expressions_to_mention

        for expression in expressions[1:-1]:
            expressions_to_mention += f', "*{expression}*"'

        return expressions_to_mention + f' e "*{expressions[-1]}*"'

    def _build_explanation(self, patterns: str) -> str:

        feedbacks_to_give = self.__feedbacks_to_give(patterns)

        return self.__default_text["explanation"].replace(
            "<feedback>", feedbacks_to_give
        )

    def __feedbacks_to_give(self, patterns):
        if len(patterns) == 1:
            return self.__explanations[patterns[0]]

        feedbacks_to_give = "\n"
        for pattern in patterns:
            feedbacks_to_give += (
                f"\n:arrow_right: {self.__explanations[pattern]}"
            )

        return feedbacks_to_give

    def _build_goodbye(self) -> str:
        return self.__default_text["goodbye"]
