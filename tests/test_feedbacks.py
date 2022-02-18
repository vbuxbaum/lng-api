import pytest
from feedbacks.feedbacks import Feedbacks


def test_instantiate_feedback_handler(feedback_handler):
    assert isinstance(feedback_handler, Feedbacks)


def test_find_avoided_expressions_with_bad_messages(
    bad_messages, feedback_handler
):
    for expression, message in bad_messages:
        assert feedback_handler.find_avoided_expression(message) == expression


def test_find_avoided_expressions_with_good_messages(
    good_messages, feedback_handler
):
    for message in good_messages:
        assert feedback_handler.find_avoided_expression(message) is None


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
