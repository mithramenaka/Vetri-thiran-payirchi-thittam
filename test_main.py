from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["application"] == "EduGenie"


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text

    assert "Learning Assistant" in response.text


def test_invalid_qa_request():

    response = client.post(
        "/qa",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_invalid_quiz_request():

    response = client.post(
        "/quiz",
        json={
            "text": "short"
        }
    )

    assert response.status_code == 422