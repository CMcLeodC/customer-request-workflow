from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyse_missing_customer_request():
    response = client.post("/requests/999/analysis")

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer request not found"


def test_create_request_analysis():
    payload = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "concon@gmail.com",
        "request_text": "I want to practice building APIs"
        }

    create_response = client.post("/requests", json=payload)

    assert create_response.status_code == 201

    request_id = create_response.json()["id"]

    analysis_response = client.post(
        f"/requests/{request_id}/analysis"
    )

    assert analysis_response.status_code == 201

    data = analysis_response.json()

    assert isinstance(data["id"], int)
    assert data["customer_request_id"] == request_id
    assert data["summary"] == payload["request_text"]
    assert data["category"] == "other"
    assert data["suggested_urgency"] == "medium"
    assert data["implementation_notes"] == "Manual review required"


def test_reject_duplicate_request_analysis():
    payload = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "connor@gmail.com",
        "request_text": "I want to practice building APIs"
        } 

    create_response = client.post("/requests", json=payload)

    assert create_response.status_code == 201

    request_id = create_response.json()["id"]
    analysis_url = f"/requests/{request_id}/analysis"

    first_analysis_response = client.post(analysis_url)

    assert first_analysis_response.status_code == 201

    second_analysis_response = client.post(analysis_url)

    assert second_analysis_response.status_code == 409
    assert second_analysis_response.json() == {
        "detail": "Request analysis already exists"
    }