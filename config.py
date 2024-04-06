from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

@dataclass
class Config:
    dotenv_path: str = field(default_factory=lambda: os.path.join(os.path.dirname(__file__), '.devcontainer', '.env'))
    broker_url: str = field(init=False)
    result_backend: str = None  # Specify if you have a result backend
    accept_content: list = field(default_factory=lambda: ['json'])
    task_serializer: str = 'json'
    result_serializer: str = 'json'
    MIN_PYRO_USER_AWS_ACCESS_KEY: str = field(init=False)
    MIN_PYRO_USER_AWS_SECRET_KEY: str = field(init=False)

    def __post_init__(self):
        load_dotenv(self.dotenv_path)
        self.broker_url = os.getenv("BROKER_URL")
        self.MIN_PYRO_USER_AWS_ACCESS_KEY = os.getenv('MIN_PYRO_USER_AWS_ACCESS_KEY')
        self.MIN_PYRO_USER_AWS_SECRET_KEY = os.getenv('MIN_PYRO_USER_AWS_SECRET_KEY')
