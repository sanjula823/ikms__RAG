"""
Tool definitions for the agent graph.
Retrieval tool for querying Pinecone vector store.
"""
from langchain_core.tools import tool
from langchain_core.documents import Document
from src.app.core.retrieval.vector_store import VectorStoreManager


# Initialize vector store manager
vector_store_manager = VectorStoreManager()


@tool
def retrieval_tool(query: str, top_k: int = 5) -> str:
    """
    Retrieve relevant documents from the vector store.
    
    Args:
        query: The search query
        top_k: Number of results to return
        
    Returns:
        Formatted string of retrieved documents with metadata
    """
    try:
        docs = vector_store_manager.retrieve(query, k=top_k)
        if not docs:
            return "No relevant documents found."
        
        results = []
        for i, doc in enumerate(docs, 1):
            page = doc.metadata.get("page", "unknown")
            source = doc.metadata.get("source", "unknown")
            results.append(
                f"Document {i} (Page {page}, Source: {source}):\n{doc.page_content}"
            )
        
        return "\n\n".join(results)
    except Exception as e:
        return f"Error retrieving documents: {str(e)}"


def get_retrieval_tool():
    """Get the retrieval tool for the agent."""
    return retrieval_tool
