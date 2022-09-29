from fastapi.testclient import TestClient


def test_endpoint(app_instance: TestClient):
    res = app_instance.get("/?input_text=classic")
    assert res.status_code == 200
    assert res.json() == []
