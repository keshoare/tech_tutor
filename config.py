import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # ✅ DEFAULT MODEL (Fast - 8B parameters)
    # Change this to "llama-3.3-70b-versatile" for smarter but slower responses
    MODEL_NAME = "llama-3.1-8b-instant"
    
    TEMPERATURE = 0.2
    MAX_TOKENS = 2048
    SAVE_DIR = "generated_code"
    
    # Ensure save directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
