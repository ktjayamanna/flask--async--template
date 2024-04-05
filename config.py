# Relative path: config.py
import os

class Config:
    BROKER_URL = os.getenv("BROKER_URL")
    AWS_ACCESS_KEY_ID = os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
    S3_BUCKET_NAME = 'workingdir--storage'
