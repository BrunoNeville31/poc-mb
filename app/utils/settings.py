from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://root:mongo123@localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "test")


settings = Settings()