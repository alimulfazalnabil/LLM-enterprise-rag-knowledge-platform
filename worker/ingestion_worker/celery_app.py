from celery import Celery

celery_app = Celery('ingestion_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/1')


@celery_app.task(name='ingestion.process_document')
def process_document(document_id: str, tenant_id: str) -> dict[str, str]:
    return {
        'document_id': document_id,
        'tenant_id': tenant_id,
        'status': 'PROCESSING',
    }
