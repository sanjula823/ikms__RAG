"""
LangGraph state machine for citation-aware RAG pipeline.
Orchestrates retrieval, generation, and verification agents.
Feature 4: Evidence-Aware Answers with Chunk Citations
"""
from langgraph.graph import StateGraph
from src.app.core.agents.state import QAState
from src.app.core.agents.agents import (
    retrieval_node,
    answer_generation_node,
    verification_node
)


def build_qa_graph():
    """
    Build the LangGraph StateGraph for the QA pipeline.
    
    Flow:
    1. Retrieval - fetch relevant documents
    2. Answer Generation - generate answer with citations
    3. Verification - verify answer accuracy and citations
    
    Returns:
        Compiled LangGraph StateGraph
    """
    
    # Create the graph
    graph = StateGraph(QAState)
    
    # Add nodes
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("generation", answer_generation_node)
    graph.add_node("verification", verification_node)
    
    # Set entry point
    graph.set_entry_point("retrieval")
    
    # Add edges (linear flow)
    graph.add_edge("retrieval", "generation")
    graph.add_edge("generation", "verification")
    
    # Set finish point
    graph.set_finish_point("verification")
    
    # Compile the graph
    compiled_graph = graph.compile()
    
    return compiled_graph


# Global graph instance
_qa_graph = None


def get_qa_graph():
    """Get or create the QA graph."""
    global _qa_graph
    if _qa_graph is None:
        _qa_graph = build_qa_graph()
    return _qa_graph
