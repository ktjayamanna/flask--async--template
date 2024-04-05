from celery import Celery
import json
from config import *
from business_logic import perform_addition, upload_to_s3

# Initialize Celery
celery = Celery('tasks', broker=CELERY_BROKER_URL)
celery.conf.update(
    CELERY_ACCEPT_CONTENT=CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
)

@celery.task(bind=True)
def add(self, x, y):
    result = perform_addition(x, y)
    result_data = json.dumps({'result': result})
    
    # Generate an object key for the S3 bucket
    object_key = f"results/{self.request.id}.json"
    bucket_name = 'your_bucket_name_here'  # Replace with your actual bucket name
    
    # Upload the result data to S3 and return the URL or key for client access
    upload_result = upload_to_s3(bucket_name, object_key, result_data)
    return upload_result
