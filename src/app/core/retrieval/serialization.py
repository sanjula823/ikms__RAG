"""
Serialization module for converting documents to context strings with chunk IDs and citations.
Feature 4: Evidence-Aware Answers with Chunk Citations
"""
from langchain_core.documents import Document


def serialize_chunks_with_ids(docs: list[Document]) -> tuple[str, dict]:
    """
    Convert retrieved documents into a context string with stable chunk IDs
    and generate a citation map.
    
    Args:
        docs: List of retrieved Document objects
        
    Returns:
        Tuple of (context_string, citation_map)
        where citation_map is {chunk_id -> {page, snippet, source}}
    """
    context_parts = []
    citation_map = {}
    
    for i, doc in enumerate(docs):
        chunk_id = f"C{i+1}"
        page = doc.metadata.get("page", "unknown")
        source = doc.metadata.get("source", "unknown")
        
        # Create the context part with chunk ID prefix
        context_part = f"[{chunk_id}] Chunk from page {page}:\n{doc.page_content}"
        context_parts.append(context_part)
        
        # Create citation metadata
        citation_map[chunk_id] = {
            "page": page,
            "snippet": doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content,
            "source": source,
            "full_content": doc.page_content
        }
    
    context_string = "\n\n".join(context_parts)
    return context_string, citation_map


def extract_citations_from_answer(answer: str, citation_map: dict) -> dict:
    """
    Extract cited chunk IDs from an answer and validate them against the citation map.
    
    Args:
        answer: Generated answer with inline citations like [C1], [C2]
        citation_map: Available citations from retrieved chunks
        
    Returns:
        Dictionary of cited chunk IDs with their metadata
    """
    import re
    
    citations = {}
    # Find all [Cn] patterns in the answer
    cite_pattern = r'\[C\d+\]'
    cited_ids = re.findall(cite_pattern, answer)
    
    for cite_id in set(cited_ids):
        # Remove brackets to get the ID
        clean_id = cite_id.strip('[]')
        if clean_id in citation_map:
            citations[clean_id] = citation_map[clean_id]
    
    return citations
