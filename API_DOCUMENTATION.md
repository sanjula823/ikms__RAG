# API Documentation

## IKMS Multi-Agent RAG API Reference

### Base URL

```
http://localhost:8000
```

For production deployment:
```
http://<your-domain>:8000
```

---

## Endpoints

### 1. POST /qa

**Answer a question with citations**

#### Request

```http
POST /qa HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "query": "What are the main indexing strategies in vector databases?",
  "top_k": 5
}
```

**Parameters:**
- `query` (string, required): User's question
- `top_k` (integer, optional): Number of chunks to retrieve (default: 5)

#### Response

**Success (200 OK):**
```json
{
  "answer": "Vector databases use several indexing strategies. HNSW provides fast approximate search through hierarchical graphs [C1][C2]. LSH uses hash functions for similarity [C4]. IVF partitions the vector space into clusters [C3].",
  "context": "[C1] Chunk from page 5:\nHNSW (Hierarchical Navigable Small World) graphs provide logarithmic search complexity...\n\n[C2] Chunk from page 6:\n...",
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
    "C3": {
      "page": 8,
      "snippet": "Inverted File (IVF) indexing partitions vectors into Voronoi cells...",
      "source": "vector_db_paper.pdf"
    },
    "C4": {
      "page": 7,
      "snippet": "Locality-Sensitive Hashing (LSH) maps similar vectors to the same hash buckets...",
      "source": "vector_db_paper.pdf"
    }
  }
}
```

**Error (500 Internal Server Error):**
```json
{
  "detail": "Error processing question: <error message>"
}
```

#### Example Requests

**Using cURL:**
```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"query": "What are vector databases?", "top_k": 5}'
```

**Using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/qa',
    json={
        'query': 'What are vector databases?',
        'top_k': 5
    }
)
data = response.json()
print(f"Answer: {data['answer']}")
print(f"Citations: {list(data['citations'].keys())}")
```

**Using JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/qa', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What are vector databases?',
    top_k: 5
  })
});

const data = await response.json();
console.log(data.answer);
console.log(data.citations);
```

---

### 2. POST /index-pdf

**Index a PDF file into the vector store**

#### Request

```http
POST /index-pdf HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "file_path": "/path/to/document.pdf"
}
```

**Parameters:**
- `file_path` (string, required): Absolute path to PDF file

#### Response

**Success (200 OK):**
```json
{
  "success": true,
  "message": "Successfully indexed 42 chunks from /path/to/document.pdf",
  "chunks_indexed": 42
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Error indexing PDF: File not found"
}
```

#### Example Requests

**Using cURL:**
```bash
curl -X POST http://localhost:8000/index-pdf \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/data/mybook.pdf"}'
```

**Using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/index-pdf',
    json={'file_path': '/data/mybook.pdf'}
)
result = response.json()
print(f"Indexed {result['chunks_indexed']} chunks")
```

**Using JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/index-pdf', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    file_path: '/data/mybook.pdf'
  })
});

const result = await response.json();
console.log(`Indexed ${result.chunks_indexed} chunks`);
```

---

### 3. GET /health

**Health check endpoint**

#### Request

```http
GET /health HTTP/1.1
Host: localhost:8000
```

#### Response

**Success (200 OK):**
```json
{
  "status": "healthy"
}
```

#### Example

```bash
curl http://localhost:8000/health
```

---

### 4. GET /info

**Get system information and features**

#### Request

```http
GET /info HTTP/1.1
Host: localhost:8000
```

#### Response

**Success (200 OK):**
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
  "endpoints": {
    "POST /qa": "Answer a question with citations",
    "POST /index-pdf": "Index a PDF file",
    "GET /health": "Health check",
    "GET /info": "System information"
  }
}
```

#### Example

```bash
curl http://localhost:8000/info
```

---

## Response Models

### QAResponse

```json
{
  "answer": "string",
  "context": "string",
  "citations": {
    "C1": {
      "page": "int | string",
      "snippet": "string",
      "source": "string"
    }
  }
}
```

**Fields:**
- `answer`: Generated answer with inline citations [C1], [C2], etc.
- `context`: Retrieved context with chunk IDs [Cn]
- `citations`: Machine-readable citation mappings

### CitationMetadata

```json
{
  "page": 5,
  "snippet": "Text excerpt from the chunk...",
  "source": "document_name.pdf"
}
```

**Fields:**
- `page`: Page number where the chunk appears
- `snippet`: First 150 characters of the chunk
- `source`: File name of the source document

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Error message describing the problem"
}
```

**Possible causes:**
- Invalid file path in `/index-pdf`
- Malformed JSON request
- Missing required fields

### 500 Internal Server Error

```json
{
  "detail": "Error processing question: <error details>"
}
```

**Possible causes:**
- Pinecone connection failure
- OpenAI API error
- Invalid PDF file format

---

## Authentication

Currently, the API does **not require authentication**. For production:

1. Add API key validation
2. Implement JWT tokens
3. Use OAuth2 with authorization

---

## Rate Limiting

Not currently implemented. Recommended for production:

```
100 requests per minute per IP address
```

---

## CORS Configuration

Configured for all origins (`*`). For production, restrict to:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)
```

---

## Citation Format Specification

### In Answer

Citations appear immediately after the claim:

```
"Vector databases provide fast search [C1]. HNSW is a popular indexing method [C2][C3]."
```

**Rules:**
- Format: `[C<number>]`
- Multiple citations: `[C2][C3]`
- One citation per claim (or related claims)
- Valid chunk IDs only (must exist in citation_map)

### In API Response

```json
{
  "citations": {
    "C1": {
      "page": 5,
      "snippet": "...",
      "source": "..."
    },
    "C2": {
      "page": 6,
      "snippet": "...",
      "source": "..."
    }
  }
}
```

---

## Integration Examples

### React Component

```jsx
import { answerQuestion } from './api';

function QAComponent() {
  const [answer, setAnswer] = useState('');
  const [citations, setCitations] = useState(null);

  const handleQuery = async (query) => {
    const response = await answerQuestion(query);
    setAnswer(response.answer);
    setCitations(response.citations);
  };

  return (
    <div>
      <input onChange={(e) => handleQuery(e.target.value)} />
      <div>{answer}</div>
      <CitationPanel citations={citations} />
    </div>
  );
}
```

### Python Application

```python
from src.app.services.qa_service import get_qa_service

service = get_qa_service()

response = service.answer_question("What are vector databases?")
print(f"Answer: {response.answer}")

for chunk_id, metadata in response.citations.items():
  print(f"{chunk_id}: Page {metadata['page']} - {metadata['source']}")
```

---

## Performance Benchmarks

Typical response times (with 5-chunk retrieval):

| Operation | Time |
|-----------|------|
| Retrieval | 200-500ms |
| Generation | 2-5s |
| Verification | 1-3s |
| **Total** | **3-8s** |

**Optimization tips:**
- Reduce `top_k` for faster retrieval
- Use smaller chunk sizes
- Cache frequent queries
- Use faster LLM models (e.g., gpt-3.5-turbo instead of gpt-4)

---

## Best Practices

1. **Query Formatting**: Use clear, specific questions
2. **Citation Validation**: Always verify that citations match the answer
3. **Error Handling**: Implement retry logic for network failures
4. **Monitoring**: Log all requests and responses
5. **Security**: Never expose API keys; use environment variables

---

## Troubleshooting

### Common Issues

**Q: No citations in response**
- A: Check that LLM is following ANSWER_GENERATION_PROMPT
- Update system prompt if needed

**Q: Invalid citations (not in citation_map)**
- A: Verify chunk IDs are stable (C1, C2, C3...)
- Check serialization.py implementation

**Q: PDF indexing fails**
- A: Verify file path is absolute
- Check file permissions
- Ensure PDF is readable (not encrypted)

**Q: Slow responses**
- A: Reduce top_k parameter
- Check Pinecone connection
- Monitor OpenAI API latency

---

## Support

For API issues:
1. Check error message details
2. Verify credentials in `.env`
3. Review logs in `logs/` directory
4. Check DEVELOPMENT.md for implementation details

---

*Last Updated: 2025-01-15*
