import time
"""Document Classification Service - Hybrid ML + Rule-based"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import logging
from app.services.mlflow_tracker import MLflowTracker
from app.data.training_data import TRAINING_DOCUMENTS

logger = logging.getLogger(__name__)

class DocumentClassifier:
    def __init__(self):
        self.categories = list(TRAINING_DOCUMENTS.keys())
        self.keyword_signals = {
            'resume': ['resume', 'cv', 'work experience', 'education', 'skills', 'professional summary'],
            'invoice': ['invoice', 'bill', 'payment', 'amount due', 'total', 'tax', 'due date'],
            'contract': ['agreement', 'contract', 'terms', 'whereas', 'termination', 'governing law', 'parties agree'],
            'letter': ['dear', 'sincerely', 'regards', 'writing to', 'thank you', 'looking forward'],
            'report': ['report', 'analysis', 'findings', 'conclusion', 'executive summary', 'recommendations']
        }
        
        self.train_data = []
        self.train_labels = []
        for category, documents in TRAINING_DOCUMENTS.items():
            for doc in documents:
                self.train_data.extend([doc, doc.lower(), doc[:len(doc)//2], doc[len(doc)//2:]])
                self.train_labels.extend([category] * 4)
        
        logger.info(f"Training with {len(self.train_data)} examples")
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1,4), min_df=1, max_df=0.9)),
            ('clf', GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42))
        ])
        self.pipeline.fit(self.train_data, self.train_labels)
        accuracy = accuracy_score(self.train_labels, self.pipeline.predict(self.train_data))
        logger.info(f"Training accuracy: {accuracy:.2%}")
        self.mlflow_tracker = MLflowTracker()
    
    def classify(self, text: str) -> dict:
        if not text or len(text.strip()) < 10:
            return {'category': 'Unknown', 'confidence': 0.0, 'all_scores': {}}
        try:
            text_lower = text.lower()
            keyword_counts = {cat: sum(1 for kw in keywords if kw in text_lower) 
                            for cat, keywords in self.keyword_signals.items()}
            max_keywords = max(keyword_counts.values())
            
            ml_probs = self.pipeline.predict_proba([text])[0]
            ml_scores = {cat: float(ml_probs[idx])*100 for idx, cat in enumerate(self.pipeline.classes_)}
            
            if max_keywords >= 3:
                best_cat = max(keyword_counts, key=keyword_counts.get)
                confidence = 75 + (keyword_counts[best_cat] * 5)
                scores = {cat: (min(confidence,95) if cat==best_cat else ml_scores.get(cat,1)*0.2) 
                         for cat in self.categories}
            else:
                scores = {cat: ml_scores.get(cat,0) + keyword_counts.get(cat,0)*12 
                         for cat in self.categories}
            
            total = sum(scores.values())
            scores = {k: (v/total)*100 for k,v in scores.items()} if total>0 else scores
            best = max(scores, key=scores.get)
            
            result = {'category': best.title(), 'confidence': round(scores[best],2),
                     'all_scores': {k: round(v,2) for k,v in scores.items()}}
            try:
                self.mlflow_tracker.log_classification(text[:50], result)
            except: pass
            return result
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {'category': 'Unknown', 'confidence': 0.0, 'all_scores': {}}

_classifier = None
def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = DocumentClassifier()
    return _classifier
