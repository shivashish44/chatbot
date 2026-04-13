import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", "18560802"))
    API_HASH = os.getenv("API_HASH", "601efbf55509f036b97e2de0cfecd827")
    OWNER_ID = int(os.getenv("OWNER_ID", "8418584090"))
    
    DATABASE_URL = "chatbot.db"
    AI_API_KEY = os.getenv("AI_API_KEY", "xai-Ej1RJYVhX3owYVT5XW81SIAc4Y72XLxAHlb9GVpQcJKI4q0ERTlJpf1iWIXxaLGqf0Vz9M99TIgn5WE8")
    AI_MODEL = os.getenv("AI_MODEL", "grok-beta")
    
    MAX_MSG_LENGTH = 4000
    DAILY_LIMIT = 1000
