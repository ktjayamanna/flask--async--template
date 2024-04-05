from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.devcontainer', '.env')
load_dotenv(dotenv_path)

CELERY_BROKER_URL = os.getenv("BROKER_URL")
CELERY_RESULT_BACKEND = None  # Specify if you have a result backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
