"""
QA Service - Facade over the LangGraph QA pipeline.
Handles question-answering with citation generation.
Feature 4: Evidence-Aware Answers with Chunk Citations
"""
from src.app.core.agents.state import QAState
from src.app.core.agents.graph import get_qa_graph
from src.app.models import QAResponse, CitationMetadata
from src.app.core.retrieval.vector_store import VectorStoreManager


class QAService:
    """Service for handling QA operations with citations."""
    
    def __init__(self):
        """Initialize the QA service."""
        self.graph = get_qa_graph()
        self.vector_store = VectorStoreManager()
    
    def answer_question(self, query: str) -> QAResponse:
        """
        Answer a question using the citation-aware RAG pipeline.
        
        Args:
            query: User's question
            
        Returns:
            QAResponse with answer, context, and citations
        """
        # Initialize state
        initial_state = QAState(query=query)
        
        # Run the graph
        result_state = self.graph.invoke(initial_state)
        
        # Convert citations to CitationMetadata objects
        citations_dict = None
        if result_state.citations:
            citations_dict = {}
            for chunk_id, metadata in result_state.citations.items():
                # Remove full_content from the response (only keep snippet)
                metadata_copy = {k: v for k, v in metadata.items() if k != 'full_content'}
                citations_dict[chunk_id] = metadata_copy
        
        # Build response
        response = QAResponse(
            answer=result_state.answer,
            context=result_state.context_string,
            citations=citations_dict
        )
        
        return response
    
    def index_pdf(self, file_path: str) -> dict:
        """
        Index a PDF file into the vector store.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with indexing results
        """
        try:
            num_chunks = self.vector_store.index_pdf(file_path)
            return {
                "success": True,
                "message": f"Successfully indexed {num_chunks} chunks from {file_path}",
                "chunks_indexed": num_chunks
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error indexing PDF: {str(e)}",
                "chunks_indexed": 0
            }


# Global service instance
_qa_service = None


def get_qa_service() -> QAService:
    """Get or create the QA service."""
    global _qa_service
    if _qa_service is None:
        _qa_service = QAService()
    return _qa_service
