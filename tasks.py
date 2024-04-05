# Relative path: tasks.py
from celery import current_app as celery_app
from business_logic import add
from utils import upload_to_s3
import json

@celery_app.task(bind=True)
def add_task(self, x, y):
    print("Yo I am here at tasks")

    result = add(x, y)
    result_data = json.dumps({'result': result})
    object_key = f"tests/{self.request.id}.json"
    upload_to_s3(object_key, result_data)
    return f"S3 Object Key: {object_key}"
