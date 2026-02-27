import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Calculate the Root Directory (Project folder)
# This goes: config.py -> app -> backend -> ROOT
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"⚙️  Loading Config. Looking for .env at: {ENV_PATH}")

class Settings(BaseSettings):
    # Elastic Cloud Serverless Credentials
    ELASTIC_CLOUD_ID: str = ""
    ELASTIC_API_KEY: str = ""
    ELASTIC_ENDPOINT: str = "" # Serverless URL
    
    # Inference API (External LLM)
    INFERENCE_MODEL_ID: str = "gpt-4-turbo"
    
    # App Config
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    class Config:
        env_file = str(ENV_PATH)
        case_sensitive = True
        extra = "ignore" 

settings = Settings()

# Debug Print to verify it worked
if settings.ELASTIC_ENDPOINT:
    print(f"✅ Configuration Loaded. Endpoint: {settings.ELASTIC_ENDPOINT}")
else:
    print("❌ CRITICAL: ELASTIC_ENDPOINT is missing. Check .env path!")