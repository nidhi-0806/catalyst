from celery import Celery
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import CSVRecord
from . import crud

celery_app = Celery(
    "worker",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0"
)

@celery_app.task
def process_csv(file_path: str, user_id: int):
    db: Session = SessionLocal()
    with open(file_path, 'r') as f:
        for line in f:
            crud.create_csv_record(db, line.strip(), user_id)
    db.close()
