from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_customer_request():
    payload = {
        "customer_id": "connor1234", 
        "requester_name": "connor_clements", 
        "requester_email": "connor@example.com", 
        "request_text": "I want to practice building APIs"
        }

    response = client.post("/requests", json=payload)

    assert response.status_code == 201
    assert response.json()["urgency"] == "medium"
    assert response.json()["customer_id"] == payload["customer_id"]


def test_invalid_email_in_create_customer_request():
    payload = {
        "customer_id": "connor1234", 
        "requester_name": "connor_clements", 
        "requester_email": "invalid_email", 
        "request_text": "I want to practice building APIs"
        }

    response = client.post("/requests", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == [
        "body", "requester_email"
        ]