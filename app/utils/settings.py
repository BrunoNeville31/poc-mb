from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://root:mongo123@localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "test")
    infura_url: str = os.getenv("INFURA_URL", "https://sepolia.infura.io/v3/663f007ea3574d1baf6864f9b1cbc5ee")


settings = Settings()