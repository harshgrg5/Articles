# 📰 Articles REST API Backend

A simple, lightweight, and robust REST API built using **Python 3**, **FastAPI**, and **Pydantic**. Built with full mobile app support (CORS enabled), custom error handling, unit testing, and Postman integration.

---

## 📋 Table of Contents
1. [Features](#-features)
2. [Active Endpoints](#-active-endpoints)
3. [Quickstart Setup](#-quickstart-setup)
4. [Running the API Server](#-running-the-api-server)
5. [API Examples](#-api-examples)
6. [Testing with Postman](#-testing-with-postman)
7. [Running Automated Tests](#-running-automated-tests)

---

## ✨ Features

- **`GET /articles`**: List all articles with optional search filtering (`prompt`, `search`) and pagination (`limit`, `offset`).
- **`GET /articles/{id}`**: Retrieve single article by ID with validation and structured 404 handling.
- **`POST /articles`**: Create a new article with payload validation.
- **Mobile Friendly**: Full CORS (`allow_origins=["*"]`) enabled out of the box for iOS and Android.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`).

---

## 🔌 Active Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/articles` | Get list of articles (with search, prompt filter, and pagination) |
| `GET` | `/articles/{id}` | Get article detail by numeric ID |
| `POST` | `/articles` | Create a new article |

---

## 🚀 Quickstart Setup & Local Server

```bash
# Run server locally
./venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- **Base URL**: `http://127.0.0.1:8000`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## 💡 API Request & Response Examples

### 1. `GET /articles`
**Request:**
```http
GET http://127.0.0.1:8000/articles
```

**Response (`200 OK`):**
```json
{
  "success": true,
  "data": [
    {
      "id": 4,
      "title": "Home office as a driver for VR Applications",
      "created_at": "2025-03-27T03:55:47.044655Z",
      "prompt": "Virtual Realms",
      "short_description": "Remote work has become the norm post-pandemic...",
      "content": "- Virtual reality (VR) creates computer-generated immersive environments...",
      "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"
    }
  ],
  "error": null,
  "meta": {
    "total": 4,
    "count": 4,
    "limit": 10,
    "offset": 0,
    "has_more": false
  }
}
```

---

### 2. `GET /articles/{id}`
**Request:**
```http
GET http://127.0.0.1:8000/articles/4
```

**Response (`200 OK`):**
```json
{
  "success": true,
  "data": {
    "id": 4,
    "title": "Home office as a driver for VR Applications",
    "created_at": "2025-03-27T03:55:47.044655Z",
    "prompt": "Virtual Realms",
    "short_description": "Remote work has become the norm post-pandemic...",
    "content": "- Virtual reality (VR) creates computer-generated immersive environments...",
    "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"
  },
  "error": null,
  "meta": null
}
```

---

## 📮 Postman & Testing

Import [`postman_collection.json`](./postman_collection.json) or run tests via CLI:

```bash
PYTHONPATH=. ./venv/bin/pytest -v
```
