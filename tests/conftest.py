from mocks import mocked_messages
from feedbacks.feedbacks import Feedbacks
import pytest


@pytest.fixture(scope="module")
def feedback_handler():
    """Instance of the main Feedback class"""

    return Feedbacks()


@pytest.fixture(scope="module")
def bad_messages():
    """Examples of messages containing avoided expression
    Format: list[tuple(avoided_expression, message_example)]"""

    return mocked_messages.BAD_MESSAGES


@pytest.fixture(scope="module")
def good_messages():
    """Examples of messages containing avoided expression
    Format: list[message_example]"""

    return mocked_messages.GOOD_MESSAGES
