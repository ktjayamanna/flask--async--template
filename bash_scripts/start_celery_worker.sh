# Relative path: bash_scripts/start_celery_worker.sh
celery -A tasks.celery worker --loglevel=debug

