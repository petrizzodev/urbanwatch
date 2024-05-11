import os 
from dotenv import load_dotenv
from pathlib import Path 


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME:str = 'UrbanWatch'
    PROJECT_VERSION:str = '1.0'
    SECRET_KEY:str = os.getenv('SECRET_KEY')
    ALGORITHM:str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    SQLALCHEMY_DATABASE_URL:str = os.getenv('SQLALCHEMY_DATABASE_URL')


settings = Settings()