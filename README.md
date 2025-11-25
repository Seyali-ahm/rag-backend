# RAG Translation Backend

A Retrieval-Augmented Translation (RAG) backend built with **FastAPI**.  
It stores translation pairs, retrieves the most similar examples with TF-IDF similarity, and exposes them via a REST API for prompt-based machine translation.

This project was developed as part of the **Junior ML Engineer Technical Test** from Translated.

---

## 🚀 Features

- **Store translation pairs** (`/pairs`)
- **Retrieve similar examples** using TF-IDF cosine similarity (`/prompt`)
- **Fully compatible with the provided `client.py` tool**
- **SQLite** for persistence (auto-created on startup)
- **Swagger UI** available at `/docs`
- **Detect stammering** in translated sentences (`/stammering`)


---

## 📂 Project Structure

```
rag-backend/
├── main.py                    # FastAPI application
├── Dockerfile                 #Dockerfile  
├── client.py                  # Provided test script
├── translation_pairs.jsonl    # Input pairs for DB population
├── translation_requests.jsonl # Input requests for prompt generation
├── stammering_tests.jsonl     # (optional) stammering tests
├── test_result.txt           # Log of running client.py
├── requirements.txt           # Python dependencies
└── README.md
```

---

## 🛠 Installation

### 1. Clone repository
```bash
git clone <repo-url>
cd rag-backend
```

### 2. Create virtual environment (recommended)

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

Interactive API docs:

- Swagger UI → http://127.0.0.1:8000/docs  
- ReDoc → http://127.0.0.1:8000/redoc

---

## 🧪 Testing With `client.py`

Make sure the server is running first:

```bash
uvicorn main:app --reload
```

### Run the client tool:
```bash
python client.py
```

You will see:

```
Select an option:
1 - Populate Database
2 - Request Prompts
3 - Detect Stammering
4 - Exit
```

### ✔ Option 1 — Populate Database

loads `translation_pairs.jsonl` into backend using `/pairs`.

Example output:

```
Line 1: Added translation pair.
Line 2: Added translation pair.
...
```

### ✔ Option 2 — Request Prompts

Loads from `translation_requests.jsonl` and calls `/prompt`.

Example:

```
Line 1: Received Translation Prompt.
Translate from en to it:
Input: Good night

Examples:

Source: Good morning!
Target: Buongiorno!

Source: Good evening!
Target: Buonasera!

Source: I'm thirsty.
Target: Ho sete.
```

### (Optional) ✔ Option 3 — Detect Stammering
Loads from `stammering_tests.jsonl` and calls `/stammering` to evaluate if translation contains repetition.
Line 1: Response -> No (Expected: No)

Line 2: Response -> No (Expected: No)


## 🐳 Running with Docker (Optional)

### 1. Build the image
```bash
docker build -t rag-backend .
```

### 2. Run the container
```bash
docker run -p 8000:8000 rag-backend
```

Access inside your browser:

- http://localhost:8000  
- http://localhost:8000/docs  

---



