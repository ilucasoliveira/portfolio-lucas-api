import pytest
from fastapi.testclient import TestClient

import main
from email_service import EmailDeliveryError

client = TestClient(main.app)

VALID_MESSAGE = {
    "name": "Ana",
    "email": "ana@example.com",
    "subject": "Job opportunity",
    "message": "Hi Lucas, I would like to talk about a role.",
}


@pytest.fixture(autouse=True)
def reset_rate_limit():
    main.limiter.reset()


@pytest.fixture
def sent_messages(monkeypatch):
    sent = []
    monkeypatch.setattr(main, "send_email", sent.append)
    return sent


def test_ping_returns_ok():
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_message_is_sent(sent_messages):
    response = client.post("/message", json=VALID_MESSAGE)

    assert response.status_code == 201
    assert len(sent_messages) == 1
    assert sent_messages[0].email == "ana@example.com"


def test_invalid_email_returns_422(sent_messages):
    response = client.post("/message", json={**VALID_MESSAGE, "email": "not-an-email"})

    assert response.status_code == 422
    assert sent_messages == []


def test_short_message_returns_422(sent_messages):
    response = client.post("/message", json={**VALID_MESSAGE, "message": "Hi"})

    assert response.status_code == 422
    assert sent_messages == []


def test_whitespace_is_stripped_before_validation(sent_messages):
    response = client.post("/message", json={**VALID_MESSAGE, "name": "   "})

    assert response.status_code == 422
    assert sent_messages == []


def test_honeypot_is_silently_discarded(sent_messages):
    response = client.post("/message", json={**VALID_MESSAGE, "website": "spam.com"})

    assert response.status_code == 201
    assert sent_messages == []


def test_fourth_message_in_a_minute_is_rate_limited(sent_messages):
    for _ in range(3):
        assert client.post("/message", json=VALID_MESSAGE).status_code == 201

    response = client.post("/message", json=VALID_MESSAGE)

    assert response.status_code == 429
    assert "detail" in response.json()
    assert len(sent_messages) == 3


def test_delivery_failure_returns_503(monkeypatch):
    def failing_send(contact):
        raise EmailDeliveryError

    monkeypatch.setattr(main, "send_email", failing_send)

    response = client.post("/message", json=VALID_MESSAGE)

    assert response.status_code == 503


def test_health_check_accepts_head():
    assert client.head("/").status_code == 200
    assert client.head("/ping").status_code == 200
