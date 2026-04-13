from pyrogram import Client, idle
import asyncio
import os
from config import Config
from utils.database import db
from utils.handlers import *

app = Client(
    "ai-chatbot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

async def main():
    print("🚀 **Starting Ultra AI Chat Bot...**")
    await db.init_db()
    await app.start()
    print("✅ **Bot is Online!**")
    print("📱 **Commands:** /start | /ping")
    print("⚡ **Powered by @betabot_hub**")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
