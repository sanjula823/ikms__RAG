# IKMS Multi-Agent RAG - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Clone/Extract Project
Already in: `d:\STEMlink\AI Enginner BootCamp\ikmsRAG`

### Step 2: Configure Environment
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your keys:
# - OPENAI_API_KEY (from OpenAI)
# - PINECONE_API_KEY (from Pinecone)
# - PINECONE_ENVIRONMENT
```

### Step 3: Install Backend
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Install Frontend
```bash
cd frontend
npm install
```

### Step 5: Start Backend
```bash
# In project root with venv activated
python -m uvicorn src.app.api:app --reload
```

### Step 6: Start Frontend
```bash
# In frontend directory
npm start
```

### Step 7: Open Browser
Visit: `http://localhost:3000`

---

## 🐳 Docker Quick Start

```bash
# Setup environment
copy .env.example .env
# Edit .env with your API keys

# Build and run
docker-compose up --build

# Access:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 🧪 Test It Works

### API Test
```bash
# In PowerShell/Terminal
curl -X POST http://localhost:8000/qa `
  -H "Content-Type: application/json" `
  -d '{"query":"What is a vector database?","top_k":5}'
```

### Browser Test
1. Go to http://localhost:3000
2. Ask: "What is a vector database?"
3. See answer with citations like [C1], [C2]
4. Hover over citations to see sources
5. Click Sources tab to see all cited documents

---

## 📁 Key Files to Know

| File | Purpose |
|------|---------|
| `src/app/api.py` | API endpoints |
| `src/app/core/agents/agents.py` | AI agents |
| `src/app/core/retrieval/vector_store.py` | Vector database |
| `frontend/src/components/QAInterface.js` | Main UI |

---

## 🚀 Common Commands

```bash
# Start backend (development)
python -m uvicorn src.app.api:app --reload

# Start backend (production)
python -m uvicorn src.app.api:app --host 0.0.0.0 --port 8000

# Start frontend (development)
npm start

# Build frontend (production)
npm run build

# View logs
Get-Content logs/*.log  # Windows
tail -f logs/*.log      # Linux/Mac
```

---

## ⚙️ Environment Variables Needed

```env
OPENAI_API_KEY=sk-...              # Your OpenAI key
PINECONE_API_KEY=...               # Your Pinecone key
PINECONE_ENVIRONMENT=...           # Your Pinecone env
PINECONE_INDEX_NAME=ikms-rag       # Index name (can keep as is)
```

---

## 🆘 Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.11+)
- Check virtual environment activated: `pip list | grep fastapi`
- Check port 8000 is free

**Frontend won't load?**
- Check Node.js: `node --version` (need 18+)
- Check npm: `npm --version`
- Clear cache: `npm cache clean --force`

**Citations not showing?**
- Check backend is running
- Verify OPENAI_API_KEY in .env
- Check browser console for errors

**Can't connect to Pinecone?**
- Verify PINECONE_API_KEY
- Check PINECONE_ENVIRONMENT
- Create index if doesn't exist

---

## 📚 Full Documentation

- **README.md** - Complete overview
- **DEVELOPMENT.md** - Developer guide
- **API_DOCUMENTATION.md** - API reference
- **IMPLEMENTATION_CHECKLIST.md** - Implementation status

---

## 🎯 What This Does

1. **Indexes PDFs** - Converts documents to searchable chunks
2. **Answers Questions** - Uses AI to generate answers from documents
3. **Cites Sources** - Every answer includes [C1], [C2] citations
4. **Shows Evidence** - Click citations to see source excerpts
5. **Visualizes Citations** - Heatmap shows most-used sources

---

## 🔄 Typical Workflow

1. **Upload Document** (via API)
   ```bash
   curl -X POST http://localhost:8000/index-pdf \
     -d '{"file_path": "document.pdf"}'
   ```

2. **Ask Question** (via UI or API)
   ```
   "What are the main topics in this document?"
   ```

3. **Get Answer with Citations**
   ```
   Answer: "The document covers topic A [C1] and topic B [C2]..."
   Citations: {
     "C1": {page: 5, source: "document.pdf"},
     "C2": {page: 8, source: "document.pdf"}
   }
   ```

4. **Verify Sources** (in UI)
   - Hover over [C1] to see snippet
   - Click Sources tab to see all
   - View heatmap of citation frequency

---

## 💡 Tips

- Use specific questions for better answers
- Citations work only if chunk contains the answer
- PDF quality affects extraction
- Larger PDFs take longer to index

---

**Ready to go?** Start with Step 1 above! 🚀
