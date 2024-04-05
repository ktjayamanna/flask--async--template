# Relative path: bash_scripts/start_celery_worker.sh
celery -A flask_async_api.celery worker --loglevel=info
