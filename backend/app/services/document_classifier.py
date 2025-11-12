"""
Document Classification Service using Machine Learning
Classifies documents into: Resume, Invoice, Contract, Letter, Report
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import re
import logging

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """ML-based document classifier"""
    
    def __init__(self):
        self.categories = {
            'resume': ['resume', 'cv', 'curriculum vitae', 'experience', 'education', 'skills', 
                      'employment', 'professional', 'qualification', 'objective', 'profile'],
            'invoice': ['invoice', 'bill', 'payment', 'amount due', 'total', 'subtotal', 
                       'tax', 'receipt', 'purchase', 'order', 'price', 'quantity'],
            'contract': ['contract', 'agreement', 'terms', 'conditions', 'party', 'hereby',
                        'whereas', 'obligations', 'termination', 'breach', 'effective date'],
            'letter': ['dear', 'sincerely', 'regards', 'yours', 'letter', 'recipient',
                      'sender', 'correspondence', 'attention', 'subject'],
            'report': ['report', 'analysis', 'findings', 'conclusion', 'summary', 'results',
                      'methodology', 'introduction', 'executive summary', 'recommendations']
        }
        
        # Create training data
        self.train_data = []
        self.train_labels = []
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                # Create sample documents with keywords
                self.train_data.append(f"{keyword} " * 10)
                self.train_labels.append(category)
        
        # Build ML pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        # Train the model
        self.pipeline.fit(self.train_data, self.train_labels)
        logger.info("Document classifier trained successfully")
    
    def classify(self, text: str) -> dict:
        """
        Classify document text
        Returns: {'category': str, 'confidence': float, 'all_scores': dict}
        """
        if not text or len(text.strip()) < 10:
            return {
                'category': 'Unknown',
                'confidence': 0.0,
                'all_scores': {}
            }
        
        # Clean text
        text = text.lower()
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Get predictions
        try:
            prediction = self.pipeline.predict([text])[0]
            probabilities = self.pipeline.predict_proba([text])[0]
            
            # Get all category scores
            all_scores = {}
            for idx, category in enumerate(self.pipeline.classes_):
                all_scores[category] = round(float(probabilities[idx]) * 100, 2)
            
            confidence = max(probabilities) * 100
            
            return {
                'category': prediction.title(),
                'confidence': round(confidence, 2),
                'all_scores': all_scores
            }
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {
                'category': 'Unknown',
                'confidence': 0.0,
                'all_scores': {}
            }
    
    def classify_by_keywords(self, text: str) -> dict:
        """Fallback: simple keyword-based classification"""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        if max(scores.values()) > 0:
            best_category = max(scores, key=scores.get)
            confidence = (scores[best_category] / sum(scores.values())) * 100
            return {
                'category': best_category.title(),
                'confidence': round(confidence, 2)
            }
        
        return {'category': 'Unknown', 'confidence': 0.0}

# Singleton
_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = DocumentClassifier()
    return _classifier
