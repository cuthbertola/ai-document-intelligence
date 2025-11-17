import mlflow
import os
from typing import Dict, Any

class MLflowTracker:
    def __init__(self):
        # Set MLflow tracking URI
        mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5001')
        mlflow.set_tracking_uri(mlflow_uri)
        mlflow.set_experiment("document_classification")
    
    def log_classification(self, document_id: str, result: Dict[str, Any]):
        """Log classification metrics to MLflow"""
        try:
            with mlflow.start_run(run_name=f"doc_{document_id}"):
                # Log parameters
                mlflow.log_param("document_id", document_id)
                mlflow.log_param("category", result.get('category', 'unknown'))
                
                # Log metrics
                mlflow.log_metric("confidence", result.get('confidence', 0.0))
                
                # Log all category scores
                all_scores = result.get('all_scores', {})
                for category, score in all_scores.items():
                    mlflow.log_metric(f"score_{category}", score)
                    
        except Exception as e:
            print(f"MLflow logging error: {e}")
