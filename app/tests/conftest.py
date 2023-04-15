import random

import pytest
import tests.mocks.mocked_messages as mocked_msgs
from src.data_model import LNGReport
from fastapi.testclient import TestClient
from src.feedback.analyzer_service import Feedbacks
from src.feedback.text_analyzer import TextAnalyzer
from src.main import app


class FakeFeedbacks:
    def __init__(self, *_) -> None:
        print("aqui")

    def find_avoided_expression(self, *_):
        return [LNGReport(used_expression="teste")]


@pytest.fixture(scope="module")
def base_report():
    return [LNGReport(used_expression="teste")]


@pytest.fixture(scope="module")
def mock_feedback():
    """Mocked instance of the main Feedback class"""

    return FakeFeedbacks()


@pytest.fixture(scope="module")
def app_instance():
    """Instance of the FastAPI app"""

    return TestClient(app=app)


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
