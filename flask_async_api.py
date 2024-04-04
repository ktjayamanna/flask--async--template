from flask import Flask, request, jsonify
from celery import Celery
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.devcontainer', '.env')
load_dotenv(dotenv_path)

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

# Define a Celery task
@celery.task
def add(x, y):
    return x + y

# Define a route to submit tasks
@app.route('/add', methods=['POST'])
def submit_add_task():
    data = request.json
    task = add.delay(data['x'], data['y'])
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(debug=True)
