"""
Core type definitions and state schemas for the IKMS RAG application.
"""
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.documents import Document


class CitationMetadata(BaseModel):
    """Metadata for a cited chunk."""
    chunk_id: str
    page: int | str
    snippet: str
    source: str


class QAResponse(BaseModel):
    """Response model for QA endpoint with citations."""
    answer: str = Field(..., description="Generated answer with inline citations")
    context: str = Field(..., description="Retrieved context with chunk IDs")
    citations: Optional[dict[str, CitationMetadata]] = Field(
        default=None,
        description="Machine-readable citation mappings (chunk_id -> metadata)"
    )


class QARequest(BaseModel):
    """Request model for QA endpoint."""
    query: str = Field(..., description="User question")
    top_k: int = Field(default=5, description="Number of chunks to retrieve")


class IndexRequest(BaseModel):
    """Request model for PDF indexing endpoint."""
    file_path: str = Field(..., description="Path to PDF file to index")
