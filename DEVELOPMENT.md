# IKMS Multi-Agent RAG - Development Guide

## Getting Started with Development

### Project Overview

This is Feature 4 (Evidence-Aware Answers with Chunk Citations) of the IKMS Multi-Agent RAG Extension Features.

The system implements a **citation-aware retrieval-augmented generation pipeline** where:
- Documents are retrieved from a vector database (Pinecone)
- Answers are generated with inline citations [C1], [C2], etc.
- Each citation maps back to a specific chunk and page
- A verification agent ensures citation accuracy

### Core Concepts

#### 1. State Management (LangGraph)

The `QAState` dataclass tracks the information flow through the pipeline:

```python
@dataclass
class QAState:
    query: str                          # User question
    retrieved_docs: list[Document]      # Documents from vector DB
    context_string: str                 # Formatted with [Cn] IDs
    citation_map: dict[str, dict]       # Cn -> {page, snippet, source}
    raw_answer: str                     # From LLM
    answer: str                         # Final answer with citations
    citations: Optional[dict[str, dict]] # Extracted citations
    is_verified: bool                   # Verification status
    verification_notes: str             # Verification details
```

#### 2. Multi-Agent Flow

```
User Query
    ↓
[RETRIEVAL] Fetch relevant chunks → create citation_map
    ↓
[GENERATION] Generate answer using [Cn] format → extract citations
    ↓
[VERIFICATION] Validate citations and accuracy
    ↓
Response with answer + citations
```

#### 3. Citation Format

- **In Context**: `[C1] Chunk from page 5:\nContent here`
- **In Answer**: `"This is true [C1]. That is also true [C2][C3]."`
- **In API Response**: `{"C1": {...metadata...}, "C2": {...}}`

### Key Implementation Files

#### Backend

| File | Purpose |
|------|---------|
| `src/app/api.py` | FastAPI endpoints |
| `src/app/models.py` | Pydantic models (QAResponse, QARequest) |
| `src/app/services/qa_service.py` | Service facade over LangGraph |
| `src/app/core/agents/state.py` | QAState dataclass |
| `src/app/core/agents/agents.py` | Agent functions (retrieval, generation, verification) |
| `src/app/core/agents/graph.py` | LangGraph StateGraph wiring |
| `src/app/core/agents/prompts.py` | System prompts for citation awareness |
| `src/app/core/retrieval/vector_store.py` | Pinecone integration |
| `src/app/core/retrieval/serialization.py` | Chunk ID generation and citation extraction |

#### Frontend

| File | Purpose |
|------|---------|
| `frontend/src/components/QAInterface.js` | Main Q&A form and result display |
| `frontend/src/components/CitationHighlight.js` | Renders citations with tooltips |
| `frontend/src/components/SourcePanel.js` | Lists all cited sources |
| `frontend/src/components/CitationHeatmap.js` | Citation frequency visualization |
| `frontend/src/api.js` | API client |

### Workflow: Processing a Question

1. **User Input**: `"What are vector databases?"`

2. **API Receives**: POST `/qa` with `{"query": "...", "top_k": 5}`

3. **QA Service Initializes**: Creates `QAState(query="...")`

4. **Graph Execution**:
   - **Retrieval Node**:
     - Queries Pinecone for similar documents
     - Sets `state.retrieved_docs`
     - Calls `serialize_chunks_with_ids()` to create `[C1]`, `[C2]`, etc.
     - Stores in `state.context_string` and `state.citation_map`
   
   - **Generation Node**:
     - Sends LLM: system prompt + context + query
     - LLM generates answer with `[C1]`, `[C2]` references
     - Stores in `state.answer`
     - Calls `extract_citations_from_answer()` to validate citations
     - Stores in `state.citations`
   
   - **Verification Node**:
     - Checks citation validity and accuracy
     - Sets `state.is_verified` and `state.verification_notes`

5. **Response Construction**:
   ```python
   QAResponse(
       answer="Vector databases use several strategies. HNSW... [C1]...",
       context="[C1] Chunk from page 5:\n...",
       citations={
           "C1": {"page": 5, "snippet": "...", "source": "..."},
           ...
       }
   )
   ```

6. **Frontend Display**:
   - Highlights citations in answer
   - Shows tooltips on hover
   - Lists sources in panel
   - Displays citation frequency heatmap

### Extending the System

#### Adding a New Agent

1. Create agent function in `src/app/core/agents/agents.py`:

```python
def my_new_node(state: QAState) -> QAState:
    """
    My new agent logic.
    """
    state.agent_logs.append("[MY_AGENT] Starting...")
    # ... implementation ...
    return state
```

2. Update graph in `src/app/core/agents/graph.py`:

```python
graph.add_node("my_agent", my_new_node)
graph.add_edge("some_node", "my_agent")
graph.add_edge("my_agent", "next_node")
```

#### Adding New Prompts

1. Add to `src/app/core/agents/prompts.py`:

```python
MY_AGENT_PROMPT = """
You are specialized for...
Remember to maintain citations [Cn]...
"""
```

2. Use in agent function:

```python
from src.app.core.agents.prompts import MY_AGENT_PROMPT

system_msg = SystemMessage(content=MY_AGENT_PROMPT)
```

#### Customizing Chunk Formatting

In `src/app/core/retrieval/serialization.py`, modify `serialize_chunks_with_ids()`:

```python
# Current format: [C1] Chunk from page 5:
# Custom format: (C1|p5) or <C1> or etc.

context_part = f"({chunk_id}|p{page}): {doc.page_content}"
```

### Frontend Component Development

#### CitationHighlight Component

```jsx
<CitationHighlight 
  text="Answer with [C1] and [C2] citations"
  citations={{
    "C1": {page: 5, snippet: "...", source: "..."},
    "C2": {page: 6, snippet: "...", source: "..."}
  }}
/>
```

Parses `[Cn]` patterns and:
- Highlights them with color
- Shows tooltip on hover
- Validates against citation_map

#### Adding New UI Features

Create new component in `frontend/src/components/`:

```jsx
// NewFeature.js
import React from 'react';
import './NewFeature.css';

const NewFeature = ({ answer, citations }) => {
  return (
    <div className="new-feature">
      {/* Your implementation */}
    </div>
  );
};

export default NewFeature;
```

Add to `QAInterface.js`:

```jsx
<div className="tab-content">
  {activeTab === 'new-feature' && (
    <NewFeature answer={answer} citations={citations} />
  )}
</div>
```

### Testing

#### Test the API

```python
import requests

# Test question answering
response = requests.post('http://localhost:8000/qa', json={
    'query': 'What is a vector database?',
    'top_k': 5
})

answer_data = response.json()
print(f"Answer: {answer_data['answer']}")
print(f"Citations found: {len(answer_data['citations'])}")

# Test PDF indexing
response = requests.post('http://localhost:8000/index-pdf', json={
    'file_path': '/path/to/document.pdf'
})
```

#### Test Citation Extraction

```python
from src.app.core.retrieval.serialization import extract_citations_from_answer

answer = "HNSW uses hierarchical graphs [C1]. LSH uses hashing [C2]."
citations_map = {
    "C1": {"page": 5, "snippet": "..."},
    "C2": {"page": 7, "snippet": "..."}
}

citations = extract_citations_from_answer(answer, citations_map)
print(citations)  # {C1: {...}, C2: {...}}
```

### Performance Considerations

1. **Chunk Size**: Larger chunks = fewer API calls but less precise citations
2. **Top-K**: More documents = better coverage but slower responses
3. **Citation Extraction**: Regex parsing is fast; validation is crucial
4. **Frontend Rendering**: Citation highlighting can be expensive with large answers

### Debugging

#### Enable Debug Logging

```env
LANGCHAIN_DEBUG=true
```

#### Check Agent Logs

```python
# In api.py after graph execution
for log in result_state.agent_logs:
    print(log)
```

#### Verify Citations

```python
# Check if all [Cn] references are in citation_map
import re
cite_pattern = r'\[C\d+\]'
cited_ids = re.findall(cite_pattern, answer)
for cite_id in cited_ids:
    assert cite_id.strip('[]') in citation_map, f"{cite_id} not found!"
```

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| LLM not using citation format | Update ANSWER_GENERATION_PROMPT with more emphasis |
| Citations point to wrong chunks | Verify chunk ordering in serialize_chunks_with_ids() |
| Missing citations in response | Check extract_citations_from_answer() regex |
| API slow | Reduce top_k, optimize LLM inference |
| Frontend tooltips not showing | Check CitationHighlight CSS z-index |

### Deployment Checklist

- [ ] Update `.env` with production API keys
- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Test with real documents via `/index-pdf`
- [ ] Run comprehensive Q&A tests
- [ ] Build frontend: `npm run build`
- [ ] Test Docker build: `docker-compose build`
- [ ] Monitor logs during initial deployment
- [ ] Set up error tracking/alerting

### Next Steps for Enhancement

1. **Implement RAG Scores**: Add relevance scores to citations
2. **Citation Confidence**: Add confidence levels to citations
3. **Context Chunking**: Implement smarter chunking strategies
4. **Answer Summarization**: Add summary agent for long answers
5. **Question Routing**: Route different query types to specialized agents
6. **Citation Analytics**: Track which citations are most useful

---

**Happy developing! Remember: Citations enable explainability.**
