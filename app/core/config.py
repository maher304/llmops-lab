from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql://llmops:llmops@localhost:5433/llmops"
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama2"
    mlflow_tracking_uri: str = "http://localhost:5000"
    deterministic_mode: bool = True
    log_level: str = "INFO"
    database_path: str = "./data/llmops.db"
    
settings = Settings()
