"""
Vector store configuration and management for Pinecone.
Handles PDF indexing and document retrieval.
"""
import os
from typing import Optional
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import pinecone


class VectorStoreManager:
    """Manages Pinecone vector store operations."""
    
    def __init__(self):
        """Initialize vector store with Pinecone and OpenAI embeddings."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "ikms-rag")
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.api_key,
            model="text-embedding-3-small"
        )
        
        # Initialize Pinecone client
        pinecone.init(api_key=self.pinecone_api_key, environment=self.pinecone_env)
        self.index = pinecone.Index(self.index_name)
    
    def index_pdf(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> int:
        """
        Load a PDF and index its contents into Pinecone.
        
        Args:
            file_path: Path to the PDF file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            Number of chunks indexed
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"File must be a PDF: {file_path}")
        
        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No content extracted from PDF: {file_path}")
        
        # Split into chunks
        splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )
        splits = splitter.split_documents(docs)
        
        # Generate embeddings and index
        vectors = []
        for i, doc in enumerate(splits):
            embedding = self.embeddings.embed_query(doc.page_content)
            vectors.append((
                f"doc_{i}",
                embedding,
                {
                    "text": doc.page_content,
                    "page": doc.metadata.get("page", "unknown"),
                    "source": doc.metadata.get("source", "unknown")
                }
            ))
        
        # Upload to Pinecone in batches
        batch_size = 50
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
        
        return len(splits)
    
    def retrieve(self, query: str, k: int = 5) -> list[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        # Embed the query
        query_embedding = self.embeddings.embed_query(query)
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        # Convert results to Document objects
        documents = []
        for match in results.matches:
            doc = Document(
                page_content=match.metadata.get("text", ""),
                metadata={
                    "page": match.metadata.get("page", "unknown"),
                    "source": match.metadata.get("source", "unknown"),
                    "score": match.score
                }
            )
            documents.append(doc)
        
        return documents
    
    def retrieve_with_scores(self, query: str, k: int = 5) -> list[tuple[Document, float]]:
        """
        Retrieve documents with relevance scores.
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        # Embed the query
        query_embedding = self.embeddings.embed_query(query)
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        # Convert results to (Document, score) tuples
        documents = []
        for match in results.matches:
            doc = Document(
                page_content=match.metadata.get("text", ""),
                metadata={
                    "page": match.metadata.get("page", "unknown"),
                    "source": match.metadata.get("source", "unknown")
                }
            )
            documents.append((doc, match.score))
        
        return documents

