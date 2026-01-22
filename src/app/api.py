"""
FastAPI application for the IKMS Multi-Agent RAG system.
Provides /qa and /index-pdf endpoints with citation support.
Feature 4: Evidence-Aware Answers with Chunk Citations
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import tempfile
import os
from src.app.models import QARequest, QAResponse, IndexRequest
from src.app.services.qa_service import get_qa_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="IKMS Multi-Agent RAG API",
    description="Citation-aware Question Answering with Evidence Tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/qa", response_model=QAResponse)
async def answer_question(request: QARequest) -> QAResponse:
    """
    Answer a question using the RAG pipeline with citations.
    
    Feature 4: Evidence-Aware Answers
    - Returns answer with inline citations [C1], [C2], etc.
    - Includes machine-readable citation mappings
    - Maps each citation to source chunk and page number
    
    Args:
        request: QARequest containing query and optional top_k
        
    Returns:
        QAResponse with answer, context, and citations
    """
    try:
        logger.info(f"Processing question: {request.query}")
        
        # Get QA service
        qa_service = get_qa_service()
        
        # Generate answer with citations
        response = qa_service.answer_question(request.query)
        
        logger.info(f"Generated answer with {len(response.citations or {}) } citations")
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.post("/index-pdf")
async def index_pdf(file: UploadFile = File(...)) -> dict:
    """
    Index a PDF file into the vector store.
    
    Args:
        file: PDF file to upload and index
        
    Returns:
        Dictionary with indexing results
    """
    temp_file_path = None
    try:
        logger.info(f"Indexing PDF: {file.filename}")
        
        # Validate file is PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="File must be a PDF"
            )
        
        # Save file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file_path = temp_file.name
            contents = await file.read()
            temp_file.write(contents)
        
        logger.info(f"Saved temporary file to: {temp_file_path}")
        
        # Get QA service and index PDF
        qa_service = get_qa_service()
        chunks_indexed = qa_service.vector_store.index_pdf(temp_file_path)
        
        logger.info(f"Successfully indexed {chunks_indexed} chunks from {file.filename}")
        
        return {
            "success": True,
            "filename": file.filename,
            "chunks_indexed": chunks_indexed,
            "message": f"Successfully indexed {chunks_indexed} chunks from {file.filename}"
        }
    
    except Exception as e:
        logger.error(f"Error indexing PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error indexing PDF: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")


@app.get("/info")
async def info():
    """Get information about the system and available features."""
    return {
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
