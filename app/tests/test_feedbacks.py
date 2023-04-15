import pytest
from app.feedback.analyzer_service import Feedbacks
import tests.mocks.mocked_messages as mocked_msgs


def test_instantiate_feedback_handler(feedback_handler):
    assert isinstance(feedback_handler, Feedbacks)


@pytest.mark.parametrize("expression,bad_message", mocked_msgs.BAD_MESSAGES)
def test_find_avoided_expressions_with_bad_messages(
    bad_message, expression, feedback_handler
):
    result = feedback_handler.find_avoided_expression(bad_message)
    for item in result:
        item.expression_alternatives = []
    assert result == [expression]


@pytest.mark.parametrize("good_message", mocked_msgs.GOOD_MESSAGES)
def test_find_avoided_expressions_with_good_messages(
    good_message, feedback_handler
):
    assert feedback_handler.find_avoided_expression(good_message) == []


def test_find_avoided_expressions_with_invalid_parameters(feedback_handler):
    with pytest.raises(
        TypeError, match="Argument needs to be a string, not <class 'list'>"
    ):
        feedback_handler.find_avoided_expression([123, "abc"])

    with pytest.raises(
        TypeError, match="Argument needs to be a string, not <class 'float'>"
    ):
        feedback_handler.find_avoided_expression(123.45)

    with pytest.raises(
        TypeError,
        match="Argument needs to be a string, not <class 'NoneType'>",
    ):
        feedback_handler.find_avoided_expression(None)
