import json
from fastapi.testclient import TestClient
from src.feedback.analyzer_service import Feedbacks
from src import main


def test_main_endpoint_with_no_params(app_instance: TestClient):
    res = app_instance.get("/")
    assert res.status_code == 200
    assert res.json() == []


def test_main_endpoint_with_invalid_size_input(app_instance: TestClient):
    mock_input = "test_input" * 1001
    res = app_instance.get(f"/?input_text={mock_input}")
    assert res.status_code == 422
    expected = [
        {
            "ctx": {"limit_value": 10000},
            "loc": ["query", "input_text"],
            "msg": "ensure this value has at most 10000 characters",
            "type": "value_error.any_str.max_length",
        }
    ]
    assert res.json()["detail"] == expected


def test_main_endpoint_mocking_service(
    app_instance: TestClient,
    monkeypatch,
    mock_feedback: Feedbacks,
    base_report,
):

    monkeypatch.setattr(main, "feedback_handler", mock_feedback)

    res = app_instance.get("/")

    assert base_report == res.json()


def test_custom_endpoint_mocking_service(
    app_instance: TestClient,
    monkeypatch,
    mock_feedback: Feedbacks,
    base_report,
):
    analyzer_options = {
        "feedbacks": {"fake expression": "fake_pattern"},
        "alternatives": {"fake_pattern": ["fake alt"]},
    }

    monkeypatch.setattr(main, "feedback_handler", mock_feedback)

    res = app_instance.post("/", content=json.dumps(analyzer_options))

    assert res.json() == []


def test_get_options_endpoint_mocking_service(
    app_instance: TestClient,
    monkeypatch,
    mock_feedback: Feedbacks,
):
    mock_options = {
        "feedbacks": {"fake expression": "fake_pattern"},
        "alternatives": {"fake_pattern": ["fake alt"]},
    }

    mock_feedback.options = mock_options

    monkeypatch.setattr(main, "feedback_handler", mock_feedback)

    res = app_instance.get("/analyzer_options")

    assert mock_options == res.json()
