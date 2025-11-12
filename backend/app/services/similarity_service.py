"""
Semantic Similarity Search using Sentence Transformers
Find similar documents using embeddings
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SimilaritySearchService:
    """Find similar documents using semantic embeddings"""
    
    def __init__(self):
        try:
            # Use a lightweight model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence Transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None
    
    def encode_text(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        if not self.model or not text:
            return np.array([])
        
        # Limit text length
        text = text[:1000]
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        if not self.model:
            return 0.0
        
        emb1 = self.encode_text(text1)
        emb2 = self.encode_text(text2)
        
        if len(emb1) == 0 or len(emb2) == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)
    
    def find_similar_documents(
        self, 
        query_text: str, 
        documents: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find most similar documents to query text
        Returns: List of documents with similarity scores
        """
        if not self.model or not query_text or not documents:
            return []
        
        query_embedding = self.encode_text(query_text)
        
        if len(query_embedding) == 0:
            return []
        
        similarities = []
        
        for doc in documents:
            doc_text = doc.get('extracted_text', '')
            if not doc_text:
                continue
            
            doc_embedding = self.encode_text(doc_text)
            
            if len(doc_embedding) == 0:
                continue
            
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            
            similarities.append({
                'document_id': doc.get('id'),
                'filename': doc.get('filename'),
                'similarity': float(similarity),
                'document_type': doc.get('document_type', 'Unknown'),
                'preview': doc_text[:200] + '...' if len(doc_text) > 200 else doc_text
            })
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]

# Singleton
_similarity_service = None

def get_similarity_service():
    global _similarity_service
    if _similarity_service is None:
        _similarity_service = SimilaritySearchService()
    return _similarity_service
