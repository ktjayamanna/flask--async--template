import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError
import os

# Initialize Boto3 S3 client with credentials from .env
def get_s3_client():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
    )
    return s3

def perform_addition(x, y):
    return x + y

def upload_to_s3(bucket_name, object_key, data):
    s3 = get_s3_client()
    try:
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return f"s3://{bucket_name}/{object_key}"
    except NoCredentialsError:
        return "AWS credentials not found."
    except ClientError as e:
        return f"An error occurred: {e}"
