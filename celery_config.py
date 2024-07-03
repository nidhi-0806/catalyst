from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0"
)
celery_app.conf.update(
    task_routes={
        'app.celery_worker.process_csv': {'queue': 'csv'},
    },
)
