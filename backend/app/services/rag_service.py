"""
RAG Service - Allows natural language queries over documents.
This creates embeddings and enables semantic search.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os

class RAGService:
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./data/vectors",
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        except:
            self.collection = self.chroma_client.get_collection("documents")
    
    def add_document(self, document_id: int, text: str, metadata: Dict = None):
        """Add a document to the vector store."""
        # Split text into chunks (simple splitting for now)
        chunks = self.split_text(text, chunk_size=500)
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = self.embedding_model.encode(chunk).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "document_id": document_id,
                    "chunk_index": i,
                    **(metadata or {})
                }],
                ids=[f"doc_{document_id}_chunk_{i}"]
            )
    
    def query_documents(self, query: str, n_results: int = 5) -> List[Dict]:
        """Query documents using natural language."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        return formatted_results
    
    def split_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks for embedding."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks

# Singleton instance
rag_service = RAGService()