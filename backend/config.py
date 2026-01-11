from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "ProductLaunchBot/1.0"
    
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    
    app_name: str = "Product Launch Intelligence Platform"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
