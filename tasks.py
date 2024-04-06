from celery import Celery
import json
from business_logic import perform_addition
from utils import upload_to_s3
from config import Config

config = Config()

celery = Celery('tasks', broker=config.CELERY_BROKER_URL)
celery.conf.update(
    CELERY_ACCEPT_CONTENT=config.CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER=config.CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=config.CELERY_RESULT_SERIALIZER,
)

@celery.task(bind=True)
def add(self, x, y):
    result = perform_addition(x, y)
    result_data = json.dumps({'result': result})
    
    # Generate an object key for the S3 bucket
    object_key = f"tests/{self.request.id}.json"
    bucket_name = 'workingdir--storage'
    
    # Upload the result data to S3 and return the URL or key for client access
    upload_result = upload_to_s3(bucket_name, object_key, result_data)
    return upload_result
