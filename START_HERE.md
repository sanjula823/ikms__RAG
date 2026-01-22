# Quick Start Guide - IKMS RAG Feature 4

## ✅ Your system is ready!

Run this validation to confirm everything works:

```bash
cd "d:\STEMlink\AI Enginner BootCamp\ikmsRAG"
python validate_system.py
```

Expected output:
```
✓ All checks passed! System is ready to use.
```

---

## 🚀 Start Using It (3 Steps)

### Step 1: Configure API Keys
Edit `.env`:
```bash
OPENAI_API_KEY=sk-...           # Get from https://platform.openai.com
PINECONE_API_KEY=...            # Get from https://pinecone.io
PINECONE_ENVIRONMENT=...        # From Pinecone console
PINECONE_INDEX_NAME=ikms-rag
```

### Step 2: Start the Backend
```bash
cd src
uvicorn app.api:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Test an Endpoint
Open another terminal:
```bash
curl -X GET http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

---

## 📖 Full Documentation

All guides are in the `docs/` folder:

1. **GETTING_STARTED.md** - Extended setup guide
2. **API_REFERENCE.md** - All endpoints explained
3. **ARCHITECTURE.md** - System design overview
4. **FRONTEND_SETUP.md** - React app setup
5. **DEPLOYMENT.md** - Deploy to production
6. **TROUBLESHOOTING.md** - Common problems & fixes
7. **FEATURES.md** - Feature explanation

---

## 🧪 Test the QA System

Once the server is running:

```bash
# Index a PDF
curl -X POST http://localhost:8000/index-pdf \
  -F "file=@path/to/document.pdf"

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

Response example:
```json
{
  "question": "What is the main topic?",
  "answer": "The document discusses...",
  "citations": [
    {
      "source": "document.pdf",
      "page": 1,
      "chunk_text": "...",
      "relevance_score": 0.95
    }
  ],
  "confidence": 0.92
}
```

---

## 🌐 Interactive API Docs

Once the server is running, open:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly in the browser!

---

## 📂 Project Layout

```
src/app/
├── api.py                    ← FastAPI server
├── models.py                 ← Data schemas
├── core/
│   ├── agents/              ← Multi-agent logic
│   └── retrieval/           ← Vector search
└── services/
    └── qa_service.py        ← QA orchestration

frontend/                     ← React app
docs/                         ← 7 guides
docker/                       ← Docker config
requirements.txt             ← Dependencies
.env.example                 ← Config template
```

---

## ⚡ Common Commands

```bash
# Validate system
python validate_system.py

# Start server
cd src && uvicorn app.api:app --reload

# Start frontend
cd frontend && npm start

# Check dependencies
pip list | grep -E "langchain|pinecone|fastapi"

# Run tests
python -m pytest src/app/tests/

# Docker deployment
docker-compose up --build
```

---

## 🆘 Troubleshooting

**Issue**: `ModuleNotFoundError`
- **Fix**: Run `pip install -r requirements.txt`

**Issue**: API won't start
- **Fix**: Run `python validate_system.py` to check setup

**Issue**: Pinecone connection error
- **Fix**: Check `.env` - verify `PINECONE_API_KEY` and `PINECONE_ENVIRONMENT`

**Issue**: OpenAI errors
- **Fix**: Verify `OPENAI_API_KEY` is set and valid

**See `docs/TROUBLESHOOTING.md` for more solutions**

---

## 📊 System Check

Run anytime to verify everything is working:

```bash
python validate_system.py
```

This checks:
- ✓ Python version
- ✓ All packages installed
- ✓ All modules importable
- ✓ All files present
- ✓ Environment setup

---

## 🎯 What's Included

✅ **Backend**: FastAPI with 8 endpoints  
✅ **Vector DB**: Pinecone integration  
✅ **Multi-Agent**: LangGraph orchestration  
✅ **Frontend**: React components  
✅ **Docker**: Production deployment  
✅ **Documentation**: 7 comprehensive guides  
✅ **Tests**: Validation script included  

---

## Next: Pick Your Path

### 🎓 Learn the System
→ Read `docs/ARCHITECTURE.md`

### 🏃 Get Running Fast
→ Follow steps above, then check `docs/GETTING_STARTED.md`

### 🚀 Deploy to Production
→ See `docs/DEPLOYMENT.md`

### 🐛 Something Broken?
→ Check `docs/TROUBLESHOOTING.md`

### 📚 API Integration
→ Read `docs/API_REFERENCE.md`

---

**You're all set! Happy building! 🎉**

