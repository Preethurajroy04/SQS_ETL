# Postgres database configuration
# create enum for credentials
from enum import Enum

class DBConfig(Enum):
    HOST = 'localhost'
    PORT = '5432'
    DATABASE = 'postgres'
    USER = 'postgres'
    PASSWORD = 'postgres'

class SQSConfig(Enum):
    SQS_QUEUE_URL = 'http://localhost:4566/000000000000/login-queue'




