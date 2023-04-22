from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_convo():
    response = client.get("/conversations/0")
    assert response.status_code == 200

    with open("test/lines/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_list_convos():
    response = client.get("/conversations/")
    assert response.status_code == 200

    with open("test/lines/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_list_convos_limit():
    response = client.get("/conversations/?limit=10")
    assert response.status_code == 200

    with open("test/lines/limit.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_list_convos_offset():
    response = client.get("/conversations/?offset=10")
    assert response.status_code == 200

    with open("test/lines/offset.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_script():
    response = client.get("/lines/0")
    assert response.status_code == 200

    with open("test/lines/script.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/conversations/4000000")
    assert response.status_code == 404