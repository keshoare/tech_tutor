import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # ✅ UPDATED: Use production-ready model (replaces deprecated llama3-70b-8192)
    MODEL_NAME = "llama-3.3-70b-versatile"  # Best for coding tasks
    
    # Alternative models you can swap in:
    # MODEL_NAME = "llama-3.1-8b-instant"      # Faster, cheaper option
    # MODEL_NAME = "openai/gpt-oss-120b"       # For complex reasoning
    
    TEMPERATURE = 0.2
    MAX_TOKENS = 4096
    SAVE_DIR = "generated_code"
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)