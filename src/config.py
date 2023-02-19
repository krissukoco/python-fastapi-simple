import os

class Config:
    PKG: str = "https://github.com/krissukoco/python-fastapi-simple"
    API_KEY: str = os.environ['API_KEY']
    POSTGRES_URI: str = os.environ['POSTGRES_URI']
    JWT_SECRET: str = os.environ['JWT_SECRET']