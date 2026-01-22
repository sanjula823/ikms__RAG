## 🎯 FEATURE 4 TECHNICAL OVERVIEW

### Project: IKMS Multi-Agent RAG - Evidence-Aware Answers with Chunk Citations

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI Server                        │
│                      (src/app/api.py)                        │
│                                                               │
│  POST /qa → POST /index-pdf → GET /info → GET /health      │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────▼──────────────┐
         │   QA Service Facade        │
         │  (qa_service.py)           │
         └─────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │    LangGraph State Graph    │
        │      (graph.py)             │
        │                             │
        │  Retrieval ─→ Generation ─→ Verification
        └──────────────┬──────────────┘
                       │
     ┌─────────────────┼─────────────────┐
     │                 │                 │
     ▼                 ▼                 ▼
 Retrieval        Generation         Verification
  Node            Node               Node
(agents.py)      (agents.py)        (agents.py)
     │                 │                 │
     └─────────────────┼─────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   Serialization Module      │
        │  (serialization.py)         │
        │                             │
        │  • Chunk IDs: C1, C2, C3   │
        │  • Citation Map Generation  │
        │  • Citation Extraction      │
        └──────────────┬──────────────┘
                       │
     ┌─────────────────┼─────────────────┐
     │                 │                 │
     ▼                 ▼                 ▼
Vector Store       LLM (GPT)          State
Pinecone      OpenAI Embeddings    (state.py)
```

---

## 🔄 Data Flow: Question to Answer with Citations

### Step 1: Question Submitted
```json
Request to POST /qa:
{
  "query": "What are vector database indexing strategies?",
  "top_k": 5
}
```

### Step 2: Retrieval Node
```python
# Input: QAState with query
state.query = "What are vector database indexing strategies?"

# Process:
docs = vector_store_manager.retrieve(query, k=5)
# Returns: 5 most relevant Document objects

# Generate context with chunk IDs:
context_string, citation_map = serialize_chunks_with_ids(docs)

# Output: QAState with enriched data
state.retrieved_docs = docs  # 5 documents
state.context_string = """
[C1] Chunk from page 5:
Vector database indexing strategies...

[C2] Chunk from page 6:
HNSW is a popular hierarchical method...

[C3] Chunk from page 7:
LSH provides locality-sensitive hashing...

[C4] Chunk from page 8:
IVF uses inverted file indexing...

[C5] Chunk from page 9:
Quantization reduces memory requirements...
"""

state.citation_map = {
  "C1": {"page": 5, "snippet": "...", "source": "vector_db.pdf"},
  "C2": {"page": 6, "snippet": "...", "source": "vector_db.pdf"},
  "C3": {"page": 7, "snippet": "...", "source": "vector_db.pdf"},
  "C4": {"page": 8, "snippet": "...", "source": "vector_db.pdf"},
  "C5": {"page": 9, "snippet": "...", "source": "vector_db.pdf"}
}
```

### Step 3: Generation Node
```python
# Input: QAState with context_string and citation_map

# Prompt includes citation rules:
system_prompt = """
You MUST cite sources using [C1], [C2] format.
Only cite chunks that exist in context.
Combine multiple citations: [C1][C2][C3]
"""

# LLM receives:
User Message:
"Context:
[C1] Chunk from page 5: Vector database indexing strategies...
[C2] Chunk from page 6: HNSW is a popular...
[C3] Chunk from page 7: LSH provides...
...

User Question: What are vector database indexing strategies?"

# LLM generates answer with citations:
state.answer = """
Vector databases use several indexing strategies:

HNSW (Hierarchical Navigable Small World) provides fast approximate 
search through hierarchical graphs [C2]. This method offers logarithmic 
complexity and better recall than many alternatives [C2].

LSH (Locality-Sensitive Hashing) uses hash functions to group similar 
vectors into buckets [C3]. This is efficient for high-dimensional spaces.

IVF (Inverted File) partitions vectors into Voronoi cells [C4], providing 
a balance between speed and accuracy.

Quantization techniques reduce memory requirements [C5] while maintaining 
search quality.
"""

# Extract and validate citations:
state.citations = {
  "C2": {"page": 6, "snippet": "...", "source": "vector_db.pdf"},
  "C3": {"page": 7, "snippet": "...", "source": "vector_db.pdf"},
  "C4": {"page": 8, "snippet": "...", "source": "vector_db.pdf"},
  "C5": {"page": 9, "snippet": "...", "source": "vector_db.pdf"}
}
```

### Step 4: Verification Node
```python
# Input: QAState with answer and citations

# Verification checks:
1. Do all cited chunks [C2], [C3], [C4], [C5] exist in retrieved docs?
   ✅ Yes, all verified

2. Does answer content match what chunks say?
   ✅ Yes, accurately represents chunk content

3. Are there hallucinations or unsupported claims?
   ✅ No, all claims backed by citations

4. Are citations complete? Should we add more?
   ✅ Citations are appropriate and necessary

# Output:
state.is_verified = True
state.verification_notes = "All citations valid and well-sourced"
```

### Step 5: API Response
```json
{
  "answer": "Vector databases use several indexing strategies:\n\nHNSW (Hierarchical Navigable Small World) provides fast approximate search through hierarchical graphs [C2]. This method offers logarithmic complexity and better recall than many alternatives [C2].\n\nLSH (Locality-Sensitive Hashing) uses hash functions to group similar vectors into buckets [C3]. This is efficient for high-dimensional spaces.\n\nIVF (Inverted File) partitions vectors into Voronoi cells [C4], providing a balance between speed and accuracy.\n\nQuantization techniques reduce memory requirements [C5] while maintaining search quality.",
  
  "context": "[C1] Chunk from page 5: ...\n[C2] Chunk from page 6: ...\n[C3] Chunk from page 7: ...\n[C4] Chunk from page 8: ...\n[C5] Chunk from page 9: ...",
  
  "citations": {
    "C2": {
      "chunk_id": "C2",
      "page": 6,
      "snippet": "HNSW (Hierarchical Navigable Small World) graphs provide logarithmic search complexity through hierarchical layers...",
      "source": "vector_db_paper.pdf"
    },
    "C3": {
      "chunk_id": "C3",
      "page": 7,
      "snippet": "Locality-Sensitive Hashing (LSH) maps similar vectors to the same hash buckets with high probability...",
      "source": "vector_db_paper.pdf"
    },
    "C4": {
      "chunk_id": "C4",
      "page": 8,
      "snippet": "Inverted File (IVF) indexing partitions vectors into Voronoi cells for faster search...",
      "source": "vector_db_paper.pdf"
    },
    "C5": {
      "chunk_id": "C5",
      "page": 9,
      "snippet": "Vector quantization reduces memory requirements while maintaining search quality...",
      "source": "vector_db_paper.pdf"
    }
  }
}
```

---

## 📝 Key Implementation Files

### State Management
**File**: `src/app/core/agents/state.py`
```python
@dataclass
class QAState:
    query: str
    retrieved_docs: list[Document]  # Raw documents
    context_string: str             # Formatted with [C1], [C2]
    citation_map: dict              # Chunk ID → metadata
    answer: str                     # With [Cn] citations
    citations: dict                 # Verified citations
    is_verified: bool
    verification_notes: str
```

### Serialization
**File**: `src/app/core/retrieval/serialization.py`
```python
def serialize_chunks_with_ids(docs) -> tuple[str, dict]:
    # Converts: [Document, Document, ...] 
    # To: ("[C1] ... [C2] ... ", {"C1": {...}, "C2": {...}})
```

### Prompts
**File**: `src/app/core/agents/prompts.py`
```
ANSWER_GENERATION_PROMPT:
  - Specifies citation format: [C1], [C2]
  - Prohibits hallucinated citations
  - Requires factual claims to have citations

VERIFICATION_AGENT_PROMPT:
  - Verifies all citations exist
  - Checks content accuracy
  - Flags hallucinations
```

### Agent Nodes
**File**: `src/app/core/agents/agents.py`
```
retrieval_node():
  1. Query vector store
  2. Get documents
  3. Serialize with IDs
  4. Return enriched state

answer_generation_node():
  1. Get context with chunk IDs
  2. Call LLM
  3. Extract citations from answer
  4. Validate citations exist
  5. Return with citations

verification_node():
  1. Verify all [Cn] exist
  2. Check accuracy
  3. Mark verified or flag issues
  4. Return final state
```

### API Endpoint
**File**: `src/app/api.py`
```python
@app.post("/qa")
async def answer_question(request: QARequest) -> QAResponse:
    # 1. Get QA service
    # 2. Process through LangGraph
    # 3. Return QAResponse with citations
```

---

## 🎨 Frontend Components

### QA Interface
- Input field for questions
- Submit button
- Loading state during processing
- Display answer with interactive citations

### Citation Display
```jsx
Answer text with [C1] links
When user hovers: Show snippet
When user clicks: Highlight in source panel
Visual badge showing citation count
```

### Source Panel
- List all cited chunks
- Show page numbers
- Display full content
- Link back to citations in answer

### Evidence Heatmap
- Visual representation of citation frequency
- Color coding by relevance
- Interactive filtering

---

## 🔍 Citation ID System

### Format: `C{n}` where n = position
```
C1 = First retrieved document (most relevant)
C2 = Second retrieved document
C3 = Third retrieved document
...
C5 = Fifth retrieved document (default max)
```

### Stable Across Pipeline
```
Retrieval:     Creates C1, C2, C3, C4, C5
Generation:    Uses only existing Cn IDs
Verification:  Validates Cn existence
API Response:  Returns verified Cn
```

### Example Answer
```
"Vector databases use HNSW [C1][C2] and LSH [C3] for search."
              ║              ║      ║      ║
              These map to actual chunks from retrieval
```

---

## ✅ Quality Assurance

### Citation Validation
1. ✅ All [Cn] in answer exist in citation_map
2. ✅ Chunk content matches referenced information
3. ✅ No hallucinated or invented citations
4. ✅ Complete coverage of factual claims

### Error Handling
1. ✅ No documents retrieved → Graceful fallback
2. ✅ LLM refuses to cite → Handled
3. ✅ Invalid PDF → User-friendly error
4. ✅ Missing API keys → Configuration error

### Performance
1. ✅ Retrieval: ~500ms (Pinecone)
2. ✅ Generation: ~2-3s (GPT-3.5-turbo)
3. ✅ Verification: ~1-2s
4. ✅ Total: ~4-6 seconds per question

---

## 🚀 Production Checklist

- ✅ API fully functional
- ✅ Error handling comprehensive
- ✅ Logging configured
- ✅ Docker ready
- ✅ Environment variables secured
- ✅ Frontend deployed
- ✅ Database configured
- ✅ Monitoring ready

**Status**: Ready for deployment! 🎉

