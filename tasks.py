from celery import Celery
import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError
from config import *
import os

# Initialize Celery
celery = Celery('tasks', broker=CELERY_BROKER_URL)
celery.conf.update(
    CELERY_ACCEPT_CONTENT=CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
)

# Initialize Boto3 S3 client with credentials from .env
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
)

@celery.task(bind=True)
def add(self, x, y):
    result = x + y
    result_data = json.dumps({'result': result})
    
    # Generate an object key for the S3 bucket
    object_key = f"results/{self.request.id}.json"
    bucket_name = 'your_bucket_name_here'  # Replace with your actual bucket name
    
    try:
        # Upload the result data to S3
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=result_data)
        # Optionally, you can log the response or do additional checks here
    except NoCredentialsError:
        return "AWS credentials not found."
    except ClientError as e:
        # This will catch other possible errors from boto3/S3
        return f"An error occurred: {e}"
    
    # Return the S3 object URL or key for client access
    # Note: Depending on your S3 bucket policy, this URL might not be publicly accessible.
    # You might need to generate a presigned URL or adjust the bucket policy.
    return f"s3://{bucket_name}/{object_key}"
