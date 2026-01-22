# IKMS Multi-Agent RAG

**Evidence-Aware Question Answering with Chunk Citations**

A complete implementation of Feature 4 from the IKMS Multi-Agent RAG Extension Features project, featuring a citation-aware retrieval-augmented generation pipeline.

## Overview

This project demonstrates a multi-agent RAG system that not only answers questions from retrieved documents but also provides **transparent, traceable citations** back to specific chunks and pages. Every claim in the answer is backed by evidence from the knowledge base.

### Key Features

✅ **Citation-Aware Answers** - Inline citations like [C1], [C2] in generated answers  
✅ **Evidence Mapping** - Machine-readable citation metadata with source and page numbers  
✅ **Multi-Agent Pipeline** - Retrieval, Generation, and Verification agents  
✅ **Interactive UI** - Rich React frontend with hover tooltips and citation heatmaps  
✅ **Vector Database** - Pinecone integration for semantic search  
✅ **Production Ready** - Docker deployment, comprehensive logging, error handling  

## Architecture

### Backend Components

```
src/app/
├── api.py                    # FastAPI endpoints (/qa, /index-pdf)
├── models.py                 # Pydantic request/response models
├── services/
│   └── qa_service.py        # QA pipeline facade
├── core/
│   ├── agents/
│   │   ├── agents.py        # Retrieval, Generation, Verification agents
│   │   ├── state.py         # LangGraph QAState schema
│   │   ├── graph.py         # StateGraph orchestration
│   │   ├── tools.py         # Retrieval tool for Pinecone
│   │   └── prompts.py       # System prompts for citation awareness
│   └── retrieval/
│       ├── vector_store.py  # Pinecone setup and operations
│       └── serialization.py # Chunk ID generation and citation mapping
```

### Frontend Components

```
frontend/src/
├── components/
│   ├── QAInterface.js       # Main Q&A interface
│   ├── CitationHighlight.js # Citation rendering with hover tooltips
│   ├── SourcePanel.js       # Citation source display
│   └── CitationHeatmap.js   # Citation frequency visualization
├── api.js                   # API client
└── App.js                   # React app entry point
```

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, LangChain v1.0, LangGraph
- **Vector DB**: Pinecone (semantic search)
- **LLM**: OpenAI (GPT-3.5-Turbo)
- **Frontend**: React 18, CSS3
- **Deployment**: Docker, Docker Compose

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key
- Pinecone API Key and Environment

### Quick Start

#### Windows

```bash
# Run setup script
setup.bat

# Update .env with your API keys
# Then start backend
python -m uvicorn src.app.api:app --reload

# In another terminal, start frontend
cd frontend
npm install
npm start
```

#### Linux/Mac

```bash
# Run setup script
bash setup.sh

# Update .env with your API keys
# Then start backend
python -m uvicorn src.app.api:app --reload

# In another terminal, start frontend
cd frontend
npm install
npm start
```

### Environment Configuration

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Pinecone Configuration
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
PINECONE_INDEX_NAME=ikms-rag

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

## Docker Deployment

### Build and Run

```bash
# Build and run with Docker Compose
docker-compose up --build

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:3000
```

### Environment Variables

Set in `.env` before running `docker-compose`:

```env
OPENAI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=your_env_here
```

## API Endpoints

### POST /qa

Answer a question with citations.

**Request:**
```json
{
  "query": "What are the main indexing strategies in vector databases?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Vector databases use several indexing strategies. HNSW provides fast approximate search through hierarchical graphs [C1][C2]. LSH uses hash functions for similarity [C4]. IVF partitions the vector space into clusters [C3].",
  "context": "[C1] Chunk from page 5:\n...",
  "citations": {
    "C1": {
      "page": 5,
      "snippet": "HNSW (Hierarchical Navigable Small World) graphs provide logarithmic search complexity...",
      "source": "vector_db_paper.pdf"
    },
    "C2": {
      "page": 6,
      "snippet": "The hierarchical structure allows efficient approximate nearest neighbor search...",
      "source": "vector_db_paper.pdf"
    },
    ...
  }
}
```

### POST /index-pdf

Index a PDF file into the vector store.

**Request:**
```json
{
  "file_path": "/path/to/document.pdf"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully indexed 42 chunks from document.pdf",
  "chunks_indexed": 42
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /info

System information and available features.

**Response:**
```json
{
  "system": "IKMS Multi-Agent RAG",
  "version": "1.0.0",
  "features": [
    "Citation-aware Question Answering",
    "Multi-agent Verification",
    "PDF Indexing with Pinecone",
    "Evidence Tracking"
  ],
  "endpoints": { ... }
}
```

## Feature Implementation: Citation-Aware Answers

### 1. Stable Chunk Identifiers

Chunks are assigned unique IDs (C1, C2, C3, etc.) during retrieval:

```python
# From serialization.py
def serialize_chunks_with_ids(docs: list[Document]) -> tuple[str, dict]:
    context_parts = []
    citation_map = {}
    
    for i, doc in enumerate(docs):
        chunk_id = f"C{i+1}"
        page = doc.metadata.get("page", "unknown")
        
        context_parts.append(f"[{chunk_id}] Chunk from page {page}:\n{doc.page_content}")
        citation_map[chunk_id] = {
            "page": page,
            "snippet": doc.page_content[:150],
            "source": doc.metadata.get("source", "unknown")
        }
    
    return "\n\n".join(context_parts), citation_map
```

### 2. Citation-Aware Prompts

Agents are instructed to cite sources using chunk IDs:

```python
ANSWER_GENERATION_PROMPT = """
When answering, you MUST cite your sources using the chunk IDs provided in the context.
Format: Include [C1], [C2], etc. immediately after statements derived from those chunks.

Example:
"HNSW indexing creates hierarchical graphs for efficient search [C1]. This approach
offers better recall than LSH methods [C3][C5]."
"""
```

### 3. Multi-Agent Pipeline

1. **Retrieval Agent** - Fetches relevant chunks from Pinecone
2. **Generation Agent** - Creates answer with inline citations [Cn]
3. **Verification Agent** - Validates citations and answer accuracy

```python
# Linear flow: Retrieval → Generation → Verification
graph.add_edge("retrieval", "generation")
graph.add_edge("generation", "verification")
```

### 4. Citation Extraction and Validation

Citations are automatically extracted from the answer:

```python
def extract_citations_from_answer(answer: str, citation_map: dict) -> dict:
    import re
    citations = {}
    cite_pattern = r'\[C\d+\]'
    cited_ids = re.findall(cite_pattern, answer)
    
    for cite_id in set(cited_ids):
        clean_id = cite_id.strip('[]')
        if clean_id in citation_map:
            citations[clean_id] = citation_map[clean_id]
    
    return citations
```

## Frontend Features

### Interactive Citations
- Click [C1] to highlight source chunks
- Hover over citations to see preview snippets
- Invalid citations highlighted in red

### Citation Sources Panel
- Expandable list of all cited chunks
- Shows page number and source file
- Full snippet text on expansion

### Citation Heatmap
- Visual representation of citation frequency
- Color intensity indicates usage
- Quick reference for most-cited sources

## Project Structure

```
ikmsRAG/
├── src/
│   ├── app/
│   │   ├── api.py
│   │   ├── models.py
│   │   ├── core/
│   │   │   ├── agents/
│   │   │   └── retrieval/
│   │   └── services/
│   └── __init__.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── setup.sh / setup.bat
├── .env.example
└── README.md
```

## Acceptance Criteria ✅

- [x] Answers include inline citations like [C1], [C2]
- [x] API exposes machine-readable citation mappings
- [x] Every citation corresponds to an actual retrieved chunk
- [x] Citation IDs remain stable throughout the pipeline
- [x] Verification step maintains citation accuracy
- [x] Interactive UI demonstrates all features
- [x] Error handling for invalid inputs
- [x] Production-ready deployment configuration

## Learning Objectives

Through this implementation, you'll understand:

1. **LangGraph & State Management** - Designing multi-agent workflows
2. **Prompt Engineering** - Writing citations-aware system prompts
3. **Message Organization** - Structuring context for LLM consumption
4. **Retrieval Patterns** - Vector database usage and ranking
5. **Agentic Behavior** - Agent cooperation and verification

## Development

### Testing the API

```bash
# Using curl
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What are vector databases?"}'

# Using Python
import requests

response = requests.post(
    'http://localhost:8000/qa',
    json={'query': 'What are vector databases?'}
)
print(response.json())
```

### Debugging

Enable debug logging in `.env`:
```env
LANGCHAIN_DEBUG=true
```

View logs in `logs/` directory.

## Troubleshooting

### API Connection Issues
- Ensure backend is running: `python -m uvicorn src.app.api:app --reload`
- Check REACT_APP_API_URL in frontend environment

### Pinecone Connection
- Verify API key and environment in `.env`
- Check Pinecone index exists: `PINECONE_INDEX_NAME=ikms-rag`

### Citation Extraction
- Ensure LLM is formatting citations as [C1], [C2], etc.
- Check ANSWER_GENERATION_PROMPT in prompts.py

### PDF Indexing Issues
- Verify PDF file path is absolute
- Check file permissions
- Ensure PDF is readable

## Contributing

To extend this project:

1. Add new agents in `src/app/core/agents/agents.py`
2. Update graph wiring in `src/app/core/agents/graph.py`
3. Modify prompts in `src/app/core/agents/prompts.py`
4. Add UI components in `frontend/src/components/`

## Performance Optimization

- **Caching**: Implement answer caching for common queries
- **Batch Processing**: Process multiple PDFs in parallel
- **Vector DB Indexing**: Use Pinecone's advanced indexing options
- **Frontend**: Code splitting and lazy loading

## Security Considerations

- API keys stored in `.env` (never commit)
- CORS configured for frontend domain
- Input validation on all endpoints
- Rate limiting recommended for production

## License

This project is part of the IKMS Multi-Agent RAG Extension Features educational series.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review code comments and docstrings
3. Examine the feature documentation
4. Test with sample queries and PDFs

---

**Built with LangChain, LangGraph, and Pinecone**
