"""
Celery configuration for background task processing.
This allows us to process documents without blocking the API.
"""
from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "document_processor",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.tasks.document_tasks']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Retry failed tasks
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# This is what Celery CLI looks for
celery = celery_app