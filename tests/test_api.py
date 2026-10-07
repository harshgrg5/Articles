import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_articles_structured():
    response = client.get("/articles")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)
    assert len(json_data["data"]) == 4
    assert json_data["meta"]["total"] == 4


def test_get_article_by_valid_id():
    response = client.get("/articles/4")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["id"] == 4
    assert json_data["data"]["title"] == "Home office as a driver for VR Applications"


def test_get_article_by_nonexistent_id():
    response = client.get("/articles/999")
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "NOT_FOUND"
    assert "Article with ID 999 was not found" in json_data["error"]["message"]


def test_get_article_validation_error():
    # Negative ID violates Path(gt=0)
    response = client.get("/articles/-5")
    assert response.status_code == 422
    json_data = response.json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "INVALID_INPUT"


def test_create_article():
    new_article_payload = {
        "title": "Exploring Generative AI in 2026",
        "prompt": "AI & Tech",
        "short_description": "Generative AI models have transformed software engineering and content creation.",
        "content": "Full length article content exploring modern generative AI models and multi-agent systems.",
        "image_url": "https://example.com/image.webp"
    }
    response = client.post("/articles", json=new_article_payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["title"] == "Exploring Generative AI in 2026"
    assert json_data["data"]["id"] == 5
