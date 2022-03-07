import random
import tests.mocks.mocked_messages as mocked_msgs
from feedbacks.feedbacks import Feedbacks
from feedbacks.text_analyzer import TextAnalyzer
import pytest


@pytest.fixture(scope="module")
def feedback_handler():
    """Instance of the main Feedback class"""

    return Feedbacks()


@pytest.fixture()
def random_good_message():
    return random.choice(mocked_msgs.GOOD_MESSAGES)


@pytest.fixture()
def random_bad_message():
    return random.choice(mocked_msgs.BAD_MESSAGES)


@pytest.fixture()
def analyzer_instance():
    raw_message = "verificamos pessoas estudantes comunicando usuários ativos"
    return TextAnalyzer(raw_message)
