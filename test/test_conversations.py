from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_add_conversation():
    response = client.post(
        "/movies/0/conversations/",
        json={
            "character_1_id": 0,
            "character_2_id": 1,
            "lines": [
                {
                    "character_id": 0,
                    "line_text": "test add convo"
                }
            ]
        },
    )
    assert response.status_code == 200

    with open("test/conversations/conversation.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_add_conversation2():
    response = client.post(
        "/movies/0/conversations/",
        json={
            "character_1_id": 0,
            "character_2_id": 0,
            "lines": []
        },
    )
    assert response.status_code == 422

def test_add_conversation3():
    response = client.post(
        "/movies/10000000000000/conversations/",
        json={
            "character_1_id": 0,
            "character_2_id": 1,
            "lines": []
        },
    )
    assert response.status_code == 422
