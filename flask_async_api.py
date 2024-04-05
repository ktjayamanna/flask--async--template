from flask import Flask, request, jsonify
from celery import Celery
from dotenv import load_dotenv
import os
import boto3
import json
from botocore.exceptions import NoCredentialsError

dotenv_path = os.path.join(os.path.dirname(__file__), '.devcontainer', '.env')
load_dotenv(dotenv_path)

aws_access_key_id = os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')

broker_url = os.getenv("BROKER_URL")
app = Flask(__name__)

# Configure Celery to use Amazon SQS
app.config['CELERY_BROKER_URL'] = broker_url
app.config['CELERY_RESULT_BACKEND'] = None  # Specify if you have a result backend
app.config['CELERY_ACCEPT_CONTENT'] = ['json']
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize a Boto3 S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

# Define a Celery task
@celery.task(bind=True)
def add(self, x, y):
    result = x + y
    result_data = json.dumps({'result': result})
    
    # Generate an object key for the S3 bucket
    object_key = f"tests/{self.request.id}.json"
    bucket_name = 'workingdir--storage'

    try:
        # Upload the result data to S3
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=result_data)
    except NoCredentialsError:
        return "AWS credentials not found."

    # Return the S3 object URL or key for client access
    return f"s3://{bucket_name}/{object_key}"

# Define a route to submit tasks
@app.route('/add', methods=['POST'])
def submit_add_task():
    data = request.json
    task = add.delay(data['x'], data['y'])
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(debug=True)
