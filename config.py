from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

@dataclass
class Config:
    dotenv_path: str = field(default_factory=lambda: os.path.join(os.path.dirname(__file__), '.devcontainer', '.env'))
    CELERY_BROKER_URL: str = field(init=False)
    CELERY_RESULT_BACKEND: str = None  # Specify if you have a result backend
    CELERY_ACCEPT_CONTENT: list = field(default_factory=lambda: ['json'])
    CELERY_TASK_SERIALIZER: str = 'json'
    CELERY_RESULT_SERIALIZER: str = 'json'
    MIN_PYRO_USER_AWS_ACCESS_KEY: str = field(init=False)
    MIN_PYRO_USER_AWS_SECRET_KEY: str = field(init=False)

    def __post_init__(self):
        load_dotenv(self.dotenv_path)
        self.CELERY_BROKER_URL = os.getenv("BROKER_URL")
        self.MIN_PYRO_USER_AWS_ACCESS_KEY = os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY')
        self.MIN_PYRO_USER_AWS_SECRET_KEY = os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
