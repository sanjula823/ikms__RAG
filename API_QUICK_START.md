## ✅ API ENDPOINTS - Ready to Use

Your IKMS RAG API has these endpoints:

### Available Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check - returns `{"status": "healthy"}` |
| POST | `/qa` | Ask question with citations |
| POST | `/index-pdf` | Index a PDF document |
| GET | `/info` | Get system information |
| GET | `/docs` | **Interactive Swagger UI** ← START HERE |
| GET | `/redoc` | Alternative API documentation |
| GET | `/openapi.json` | OpenAPI schema |

---

## 🚀 How to Use

### Option 1: Use Interactive API Docs (EASIEST)
1. Start server: `python -m uvicorn src.app.api:app --port 8000`
2. Open browser: **http://localhost:8000/docs**
3. Click "Try it out" on any endpoint
4. Click "Execute"

### Option 2: Test Health Check
```bash
# In another terminal:
curl http://localhost:8000/health
```

### Option 3: Ask a Question
```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "top_k": 5
  }'
```

### Option 4: Index a PDF
```bash
curl -X POST http://localhost:8000/index-pdf \
  -F "file=@path/to/your/document.pdf"
```

---

## ❓ Why You Got "Not Found"

You were likely:
1. Hitting the wrong URL (check the table above)
2. Using wrong HTTP method (POST vs GET)
3. Not starting the server correctly

### Correct Startup Command
```bash
cd "d:\STEMlink\AI Enginner BootCamp\ikmsRAG"
python -m uvicorn src.app.api:app --port 8000
```

Then visit: **http://localhost:8000/docs**

---

## ✨ What Each Endpoint Does

### GET `/health`
Quick check if server is running
```json
Response: {"status": "healthy"}
```

### POST `/qa`
Ask a question about your indexed documents
```json
Request: {
  "question": "Your question here",
  "top_k": 5
}

Response: {
  "question": "Your question",
  "answer": "Generated answer with citations",
  "citations": [...]
}
```

### POST `/index-pdf`
Upload and index a PDF document
- Upload a file
- Returns number of chunks indexed

### GET `/info`
Get system information and stats

---

## 🆘 If You Still Get "Not Found"

1. **Check server is running**:
   - You should see: `Uvicorn running on http://127.0.0.1:8000`

2. **Use the correct URL**:
   - ✅ `http://localhost:8000/health`
   - ❌ `http://localhost:8000/` (root path not defined)
   - ❌ `http://localhost:8000/api/health` (wrong path)

3. **Use Swagger UI instead**:
   - Go to: `http://localhost:8000/docs`
   - Click "Try it out" on any endpoint
   - Much easier than manual curl commands

4. **Check that server is on port 8000**:
   - Look for: `Uvicorn running on http://127.0.0.1:8000`

---

## 📋 Quick Test

```bash
# 1. Start server (in one terminal)
python -m uvicorn src.app.api:app --port 8000

# 2. In another terminal, test health endpoint
curl http://localhost:8000/health

# 3. Or open browser
# http://localhost:8000/docs
```

**That's it! Your API is working.** ✅

