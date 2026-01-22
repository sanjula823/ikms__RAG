"""
LangGraph state definitions for the citation-aware RAG pipeline.
"""
from typing import Optional
from dataclasses import dataclass, field
from langchain_core.documents import Document


@dataclass
class QAState:
    """State object for the multi-agent QA graph with citations."""
    
    # Input
    query: str
    
    # Retrieval
    retrieved_docs: list[Document] = field(default_factory=list)
    context_string: str = ""
    citation_map: dict[str, dict] = field(default_factory=dict)
    
    # Generation
    raw_answer: str = ""
    answer: str = ""
    
    # Citations
    citations: Optional[dict[str, dict]] = None
    
    # Verification
    is_verified: bool = False
    verification_notes: str = ""
    
    # Metadata
    agent_logs: list[str] = field(default_factory=list)
