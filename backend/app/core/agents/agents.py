"""
Agent definitions for the citation-aware RAG pipeline.
Implements retrieval, summarization, and verification agents.
Feature 4: Evidence-Aware Answers with Chunk Citations
"""
import json
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.app.core.agents.state import QAState
from src.app.core.agents.prompts import (
    RETRIEVAL_AGENT_PROMPT,
    ANSWER_GENERATION_PROMPT,
    VERIFICATION_AGENT_PROMPT
)
from src.app.core.retrieval.vector_store import VectorStoreManager
from src.app.core.retrieval.serialization import (
    serialize_chunks_with_ids,
    extract_citations_from_answer
)


# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
vector_store_manager = VectorStoreManager()


def retrieval_node(state: QAState) -> QAState:
    """
    Retrieval agent node: fetch relevant documents from vector store.
    """
    try:
        # Log operation
        state.agent_logs.append(f"[RETRIEVAL] Query: {state.query}")
        
        # Retrieve documents
        docs = vector_store_manager.retrieve(state.query, k=5)
        state.retrieved_docs = docs
        
        # Generate context string with chunk IDs and citation map
        context_string, citation_map = serialize_chunks_with_ids(docs)
        state.context_string = context_string
        state.citation_map = citation_map
        
        state.agent_logs.append(f"[RETRIEVAL] Retrieved {len(docs)} documents")
        
        return state
    except Exception as e:
        state.agent_logs.append(f"[RETRIEVAL ERROR] {str(e)}")
        return state


def answer_generation_node(state: QAState) -> QAState:
    """
    Answer generation agent node: generate answer with inline citations.
    """
    try:
        if not state.context_string:
            state.raw_answer = "No context retrieved. Unable to generate answer."
            state.answer = state.raw_answer
            return state
        
        state.agent_logs.append("[GENERATION] Starting answer generation")
        
        # Prepare messages
        system_msg = SystemMessage(content=ANSWER_GENERATION_PROMPT)
        context_with_query = f"Context:\n{state.context_string}\n\nUser Question: {state.query}"
        user_msg = HumanMessage(content=context_with_query)
        
        # Generate answer
        response = llm.invoke([system_msg, user_msg])
        state.raw_answer = response.content
        state.answer = response.content
        
        # Extract citations from the answer
        citations = extract_citations_from_answer(state.answer, state.citation_map)
        state.citations = citations
        
        state.agent_logs.append(f"[GENERATION] Answer generated with {len(citations)} citations")
        
        return state
    except Exception as e:
        state.agent_logs.append(f"[GENERATION ERROR] {str(e)}")
        state.answer = f"Error generating answer: {str(e)}"
        return state


def verification_node(state: QAState) -> QAState:
    """
    Verification agent node: verify answer accuracy and citation validity.
    """
    try:
        if not state.answer:
            state.verification_notes = "No answer to verify"
            state.is_verified = False
            return state
        
        state.agent_logs.append("[VERIFICATION] Starting verification")
        
        # Prepare verification prompt
        verification_context = f"""
Answer to verify:
{state.answer}

Available citations:
{json.dumps(state.citation_map, indent=2)}

Verify this answer for:
1. Citation validity (all [Cn] references exist in citation map)
2. Factual accuracy (claims match the source chunks)
3. No hallucination (no unsupported claims)
"""
        
        system_msg = SystemMessage(content=VERIFICATION_AGENT_PROMPT)
        user_msg = HumanMessage(content=verification_context)
        
        # Run verification
        response = llm.invoke([system_msg, user_msg])
        
        # Parse verification result
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                state.is_verified = result.get("is_verified", True)
                state.verification_notes = json.dumps(result, indent=2)
            else:
                # Fallback: assume verified if no issues found
                state.is_verified = "error" not in response.content.lower() and "issue" not in response.content.lower()
                state.verification_notes = response.content
        except json.JSONDecodeError:
            state.is_verified = True
            state.verification_notes = response.content
        
        state.agent_logs.append(f"[VERIFICATION] Verification complete. Verified: {state.is_verified}")
        
        return state
    except Exception as e:
        state.agent_logs.append(f"[VERIFICATION ERROR] {str(e)}")
        state.verification_notes = f"Verification error: {str(e)}"
        state.is_verified = False
        return state
