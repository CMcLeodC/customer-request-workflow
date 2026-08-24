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
    assert response.json()["id"] == 1
    assert response.json()["status"] == "new"


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


def test_get_customer_request():
    payload = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "connor@example.com",
        "request_text": "I want to practice building APIs"
        }

    response = client.post("/requests", json=payload)

    assert response.status_code == 201
    assert isinstance(response.json()["id"], int)

    request_id = response.json()["id"]

    get_response = client.get(f"/requests/{request_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == request_id
    assert get_response.json()["customer_id"] == payload["customer_id"]


def test_get_customer_request_not_found():
    response = client.get("/requests/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer request not found"}


def test_list_customer_requests():
    payload1 = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "connor@example.com",
        "request_text": "I want to practice building APIs"
        }

    payload2 = {
        "customer_id": "alex5678",
        "requester_name": "alex_johnson",
        "requester_email": "alex@example.com",
        "request_text": "I need help with my order"
        }

    client.post("/requests", json=payload1)
    client.post("/requests", json=payload2)

    response = client.get("/requests")

    assert response.status_code == 200
    assert len(response.json()) == 2

    customer_ids = {
    item["customer_id"]
    for item in response.json()
    }

    assert customer_ids == {"connor1234", "alex5678"}


def test_update_customer_request_status():
    payload = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "connor@example.com",
        "request_text": "I want to practice building APIs"
        }

    response = client.post("/requests", json=payload)

    assert response.status_code == 201
    assert isinstance(response.json()["id"], int)

    request_id = response.json()["id"]

    update_response = client.patch(f"/requests/{request_id}", json={"status": "reviewing"})
    get_response = client.get(f"/requests/{request_id}")

    assert update_response.status_code == 200
    assert update_response.json()["id"] == request_id
    assert update_response.json()["customer_id"] == payload["customer_id"]
    assert update_response.json()["status"] == "reviewing"
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "reviewing"


def test_update_customer_request_with_invalid_status():
    payload = {
        "customer_id": "connor1234",
        "requester_name": "connor_clements",
        "requester_email": "connor@example.com",
        "request_text": "I want to practice building APIs"
        }

    response = client.post("/requests", json=payload)

    assert response.status_code == 201
    assert isinstance(response.json()["id"], int)

    request_id = response.json()["id"]

    update_response = client.patch(f"/requests/{request_id}", json={"status": "banana"})

    assert update_response.status_code == 422
    assert update_response.json()["detail"][0]["loc"] == [
        "body",
        "status",
    ]


def test_update_customer_request_not_found():
    update_response = client.patch("/requests/999", json={"status": "reviewing"})

    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Customer request not found"}