from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = "postgresql://llmops:llmops@localhost:5433/llmops"
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama2"
    mlflow_tracking_uri: str = "http://localhost:5000"
    deterministic_mode: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
