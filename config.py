import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Owner ID (Your Telegram ID)
    OWNER_ID = int(os.getenv("OWNER_ID", "8418584090"))  # Change this!
    
    # Database
    DATABASE_URL = "chatbot.db"
    
    # AI API (Optional - Grok, OpenAI, etc.)
    AI_API_KEY = os.getenv("xai-Ej1RJYVhX3owYVT5XW81SIAc4Y72XLxAHlb9GVpQcJKI4q0ERTlJpf1iWIXxaLGqf0Vz9M99TIgn5WE", "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")
    AI_MODEL = os.getenv("AI_MODEL", "grok-beta")
    
    # Chat Limits
    MAX_MSG_LENGTH = 4096
    DAILY_LIMIT = 10000
