import mlflow
import os
from datetime import datetime

class MLflowTracker:
    def __init__(self):
        # Set tracking URI from environment
        mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://mlflow:5000')
        mlflow.set_tracking_uri(mlflow_uri)
        
        # Set experiment name
        try:
            mlflow.set_experiment("document-classification")
        except Exception as e:
            print(f"Warning: Could not set MLflow experiment: {e}")
    
    def log_classification(self, document_id, result):
        """Log document classification to MLflow"""
        try:
            with mlflow.start_run(run_name=f"doc_{document_id[:8]}"):
                # Log parameters
                mlflow.log_param("document_id", document_id)
                mlflow.log_param("timestamp", datetime.now().isoformat())
                
                # Log metrics
                mlflow.log_metric("confidence", result.get('confidence', 0))
                
                # Log all category scores
                if 'all_scores' in result:
                    for category, score in result['all_scores'].items():
                        mlflow.log_metric(f"score_{category}", score)
                
                # Log the predicted category as a tag
                mlflow.set_tag("predicted_category", result.get('category', 'Unknown'))
                
                print(f"✅ Logged classification to MLflow: {document_id}")
        except Exception as e:
            print(f"⚠️ Failed to log to MLflow: {e}")
