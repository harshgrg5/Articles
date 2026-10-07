# 📰 Articles REST API Backend

A simple, lightweight, and robust REST API built using **Python 3**, **FastAPI**, and **Pydantic**. Built with full mobile app support (CORS enabled), custom error handling, unit testing, Postman integration, and ngrok tunneling.

---

## 📋 Table of Contents
1. [Features](#-features)
2. [Project Structure](#-project-structure)
3. [Quickstart Setup](#-quickstart-setup)
4. [Running the API Server](#-running-the-api-server)
5. [Connecting Mobile Apps via Ngrok](#-connecting-mobile-apps-via-ngrok)
6. [API Endpoints & Examples](#-api-endpoints--examples)
7. [Testing with Postman](#-testing-with-postman)
8. [Mobile App Integration Examples](#-mobile-app-integration-examples)
9. [Running Automated Tests](#-running-automated-tests)

---

## ✨ Features

- **Raw List Endpoint (`GET /myapp/list/`)**: Returns direct JSON array `[ { "id": 4, "title": "...", ... } ]`.
- **Structured Envelope Endpoints (`GET /articles`)**: Returns clean metadata-wrapped JSON responses `{ "success": true, "data": [...], "meta": {...} }`.
- **Validation & Error Handling**: Custom handlers for `404 Not Found` and `422 Unprocessable Entity` validation errors.
- **Mobile Friendly**: Full CORS (`allow_origins=["*"]`) enabled out of the box for React Native, Flutter, Expo, iOS, and Android.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Postman Collection Included**: Pre-built [`postman_collection.json`](./postman_collection.json) ready for 1-click import.

---

## 📁 Project Structure

```text
articles-api/
├── main.py                   # FastAPI application & route definitions
├── models.py                 # Pydantic data schemas & response models
├── database.py               # In-memory repository with real VR/Metaverse sample data
├── requirements.txt          # Python package dependencies
├── postman_collection.json   # Ready-to-import Postman collection
├── tests/
│   └── test_api.py           # Pytest unit & integration test suite
└── README.md                 # Complete documentation
```

---

## 🚀 Quickstart Setup

### 1. Prerequisites
- Python 3.9+ installed on your system.

### 2. Install Dependencies
If setting up in a fresh environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

---

## 🖥️ Running the API Server

Start the server locally using Uvicorn:

```bash
./venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once started, the following URLs will be available:
- **Base URL**: `http://127.0.0.1:8000`
- **Swagger Interactive Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 🌐 Connecting Mobile Apps via Ngrok

To test the API on physical mobile devices (iOS / Android) or external networks, expose port 8000 with ngrok:

```bash
ngrok http 8000
```

You will get a public HTTPS URL like:
`https://crushed-procreate-album.ngrok-free.dev`

Use this base URL directly inside your mobile application!

---

## 🔌 API Endpoints & Examples

### 1. `GET /myapp/list/` (Direct Raw JSON Array)
Returns array of all articles.

**Request:**
```http
GET http://127.0.0.1:8000/myapp/list/
```

**Response (`200 OK`):**
```json
[
  {
    "id": 4,
    "title": "Home office as a driver for VR Applications",
    "created_at": "2025-03-27T03:55:47.044655Z",
    "prompt": "Virtual Realms",
    "short_description": "Remote work has become the norm post-pandemic...",
    "content": "- Virtual reality (VR) creates computer-generated immersive environments...",
    "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"
  },
  {
    "id": 3,
    "title": "The Future of Virtual Reality: Prepare to Be Amazed in 2023!",
    "created_at": "2025-03-27T03:55:30.815007Z",
    "prompt": "Articles",
    "short_description": "VR has evolved beyond gaming and entertainment...",
    "content": "VR gaming has reached new levels of sophistication...",
    "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-03-29_18-59-35_9996.webp"
  }
]
```

---

### 2. `GET /articles` (Structured Envelope with Search & Pagination)

**Query Parameters:**
- `search` *(optional)*: Search term matching title, short description, or content.
- `prompt` *(optional)*: Filter by prompt category (e.g. `Virtual Realms`).
- `limit` *(default: 10)*: Number of items per page.
- `offset` *(default: 0)*: Pagination offset.

**Request:**
```http
GET http://127.0.0.1:8000/articles?search=Virtual&limit=10&offset=0
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
      "short_description": "Remote work has become the norm...",
      "content": "Virtual reality (VR) creates...",
      "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"
    }
  ],
  "error": null,
  "meta": {
    "total": 4,
    "count": 1,
    "limit": 10,
    "offset": 0,
    "has_more": false
  }
}
```

---

### 3. `GET /articles/{id}` (Get Article by ID)

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

**404 Not Found Response (`GET /articles/999`):**
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Article with ID 999 was not found.",
    "details": null
  },
  "meta": null
}
```

**422 Validation Error Response (`GET /articles/-1`):**
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Request validation failed. Please check input parameters.",
    "details": {
      "errors": [
        {
          "field": "path -> id",
          "msg": "Input should be greater than 0"
        }
      ]
    }
  },
  "meta": null
}
```

---

### 4. `POST /articles` (Create New Article)

**Request:**
```http
POST http://127.0.0.1:8000/articles
Content-Type: application/json

{
  "title": "Exploring Generative AI in 2026",
  "prompt": "AI & Tech",
  "short_description": "Generative AI models have transformed software engineering.",
  "content": "Full length article content exploring modern generative AI models.",
  "image_url": "https://example.com/image.webp"
}
```

**Response (`201 Created`):**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "created_at": "2026-10-07T12:46:00.123456Z",
    "title": "Exploring Generative AI in 2026",
    "prompt": "AI & Tech",
    "short_description": "Generative AI models have transformed software engineering.",
    "content": "Full length article content exploring modern generative AI models.",
    "image_url": "https://example.com/image.webp"
  },
  "error": null,
  "meta": null
}
```

---

## 📮 Testing with Postman

1. Open **Postman**.
2. Click **Import** (top left).
3. Select [`postman_collection.json`](./postman_collection.json) from the project folder.
4. All requests are ready to execute with a single click!

*(Alternatively, paste `http://127.0.0.1:8000/openapi.json` into Postman Import).*

---

## 📱 Mobile App Integration Examples

### React Native / JavaScript (`fetch`)
```javascript
const API_URL = 'https://YOUR_NGROK_SUBDOMAIN.ngrok-free.dev/myapp/list/';

async function fetchArticles() {
  try {
    const response = await fetch(API_URL, {
      headers: {
        'ngrok-skip-browser-warning': 'true' // Bypasses ngrok warning page
      }
    });
    const articles = await response.json();
    console.log('Fetched Articles:', articles);
  } catch (error) {
    console.error('Error fetching articles:', error);
  }
}
```

### Flutter / Dart (`http`)
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<dynamic>> fetchArticles() async {
  final url = Uri.parse('https://YOUR_NGROK_SUBDOMAIN.ngrok-free.dev/myapp/list/');
  final response = await http.get(
    url,
    headers: {'ngrok-skip-browser-warning': 'true'},
  );

  if (response.statusCode == 200) {
    return json.decode(response.body);
  } else {
    throw Exception('Failed to load articles');
  }
}
```

---

## 🧪 Running Automated Tests

Run the test suite using pytest:

```bash
PYTHONPATH=. ./venv/bin/pytest -v
```

**Test Coverage:**
- Root & Health Check Endpoints
- Structured List & Detail retrieval
- 404 Not Found error formatting
- 422 Path validation constraints
- Raw array `/myapp/list/` retrieval
- `POST /articles` creation
