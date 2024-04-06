import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
from config import Config

dotenv_path = os.path.join(os.path.dirname(__file__), '.devcontainer', '.env')
load_dotenv(dotenv_path)

# Instantiate the Config object
config = Config()

def get_s3_client():
    """Initializes and returns a Boto3 S3 client using credentials from environment variables."""
    s3 = boto3.client(
        's3',
        aws_access_key_id= config.MIN_PYRO_USER_AWS_ACCESS_KEY,
        aws_secret_access_key=config.MIN_PYRO_USER_AWS_SECRET_KEY
    )
    return s3

def upload_to_s3(bucket_name, object_key, data):
    """Uploads data to an S3 bucket and returns the S3 object URL or an error message."""
    s3 = get_s3_client()
    try:
        response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return f"s3://{bucket_name}/{object_key}"
    except NoCredentialsError:
        return "AWS credentials not found."
    except ClientError as e:
        return f"An error occurred: {e}"
