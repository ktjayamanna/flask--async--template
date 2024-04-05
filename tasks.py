from celery import Celery
import json
from config import *
from business_logic import perform_addition
# from utils import upload_to_s3

import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.devcontainer', '.env')
load_dotenv(dotenv_path)
def upload_to_s3(bucket_name, object_key, data):
    """Uploads data to an S3 bucket and returns the S3 object URL or an error message."""
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
    )
    print(os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY'))

    try:
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return f"s3://{bucket_name}/{object_key}"
    except NoCredentialsError:
        return "AWS credentials not found."
    except ClientError as e:
        return f"An error occurred: {e}"

# Initialize Celery
celery = Celery('tasks', broker=CELERY_BROKER_URL)
celery.conf.update(
    CELERY_ACCEPT_CONTENT=CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
)

@celery.task(bind=True)
def add(self, x, y):
    print("Hiiii mom!!!!")
    result = perform_addition(x, y)
    result_data = json.dumps({'result': result})
    
    # Generate an object key for the S3 bucket
    print("Work is done now", self.request.id)
    object_key = f"tests/{self.request.id}.json"
    bucket_name = 'workingdir--storage'
    
    # Upload the result data to S3 and return the URL or key for client access
    upload_result = upload_to_s3(bucket_name, object_key, result_data)
    return upload_result
