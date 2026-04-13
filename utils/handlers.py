from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import asyncio
from config import Config
from utils.database import db
import requests
import json
import time
from datetime import datetime

AI_PROVIDERS = {
    "grok": "https://api.x.ai/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions"
}

async def ai_response(message: str, model: str = Config.AI_MODEL) -> str:
    """Generate AI response"""
    if not Config.AI_API_KEY:
        return "❌ **AI API Key not configured!** Contact owner."
    
    headers = {
        "Authorization": f"Bearer {Config.AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(AI_PROVIDERS.get("grok", AI_PROVIDERS["openai"]), 
                               headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return "❌ **AI API Error!** Try again later."
    except:
        return "❌ **Network Error!** Please try again."

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("💬 Chat Now", callback_data="chat")],
        [InlineKeyboardButton("🔥 Powered by @betabot_hub", url="https://t.me/betabot_hub")]
    ])

def get_ping_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Start Chat", callback_data="start_chat")],
        [InlineKeyboardButton("📈 Ping Stats", callback_data="ping_stats")],
        [InlineKeyboardButton("🚀 @betabot_hub", url="https://t.me/betabot_hub")]
    ])

@Client.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    user = message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    
    # Send Start Image with Mention
    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo="start.jpg",
            caption=f"""🎉 **Welcome {mention}!**

🔥 **Ultra AI Chat Bot** is **Online!**

✨ **Features:**
- 🤖 **Smart AI Responses**
- 👥 **Group & Channel Support** 
- 📊 **Owner Dashboard**
- ⚡ **Ultra Fast** (Powered by Railway)

💬 **Just send any message to chat!**

⚡ **Powered by @betabot_hub**""",
            reply_markup=get_start_keyboard(),
            parse_mode="Markdown"
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_photo(
            chat_id=message.chat.id,
            photo="https://i.ibb.co/sp88DZ2h/8418584090-27904.jpg",
            caption=f"🎉 **Welcome Baby  {mention}!**\n\n🔥 **Ultra AI Bot Active!**\n\n💬 Send message to start chatting!\n\n⚡ **Powered by @betabot_hub**",
            reply_markup=get_start_keyboard()
        )

@Client.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    user = message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    
    start_time = time.time()
    ping_msg = await message.reply_photo(
        photo="https://i.ibb.co/6SC161C/8418584090-28811.jpg",
        caption="🏓 **Pinging...**",
        reply_markup=get_ping_keyboard()
    )
    
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 2)
    
    # Update with final ping
    await ping_msg.edit_caption(
        f"⚡ **Pong!** `{ping_time}ms`\n\n"
        f"👤 **User:** {mention}\n"
        f"🕐 **Uptime:** {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"🚀 **Ultra Fast Bot**\n"
        f"⚡ **Powered by @betabot_hub**",
        parse_mode="Markdown"
    )

@Client.on_callback_query(filters.regex("stats"))
async def stats_callback(client: Client, callback_query):
    if callback_query.from_user.id != Config.OWNER_ID:
        return await callback_query.answer("❌ **Owner only!**", show_alert=True)
    
    async with aiosqlite.connect("chatbot.db") as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        user_count = (await cursor.fetchone())[0]
        
        cursor = await db.execute("SELECT SUM(chat_count) FROM users")
        total_chats = (await cursor.fetchone())[0] or 0
    
    await callback_query.edit_message_caption(
        f"📊 **Owner Stats**\n\n"
        f"👥 **Total Users:** `{user_count}`\n"
        f"💬 **Total Messages:** `{total_chats}`\n"
        f"⏰ **Server Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        f"⚡ **Powered by @betabot_hub**",
        parse_mode="Markdown"
    )

@Client.on_message(filters.private & filters.text & ~filters.me & ~filters.command(["start", "ping"]))
async def private_chat(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Add user to database
    await db.add_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Check daily limit
    chat_count = await db.get_user_chat_count(user_id)
    if chat_count >= Config.DAILY_LIMIT:
        user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        return await message.reply(
            f"⚠️ **Daily limit reached {user_mention}!**\n\n"
            f"📊 **Chats used:** `{chat_count}/{Config.DAILY_LIMIT}`\n"
            f"⏳ **Reset in 24h**\n\n"
            f"👨‍💼 **Contact owner for premium!**",
            parse_mode="Markdown"
        )
    
    # Increment count
    await db.increment_chat_count(user_id)
    
    # Typing + Loading
    await message.reply_chat_action("typing")
    loading_msg = await message.reply("🤖 **AI is thinking...**")
    
    # Generate response
    response = await ai_response(message.text)
    
    # Delete loading
    await loading_msg.delete()
    
    # Send response (split if too long)
    if len(response) > Config.MAX_MSG_LENGTH:
        for i in range(0, len(response), Config.MAX_MSG_LENGTH):
            await message.reply(response[i:i+Config.MAX_MSG_LENGTH])
    else:
        await message.reply(response)

@Client.on_message(filters.group & filters.text & ~filters.me)
async def group_chat(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Check if group is active
    if not await db.is_group_active(chat_id):
        return
    
    # Reply only to bot mentions or replies to bot
    bot_mention = f"@{client.me.username}" if client.me.username else None
    if (bot_mention and bot_mention in message.text) or \
       (message.reply_to_message and message.reply_to_message.from_user.is_self):
        
        await message.reply_chat_action("typing")
        loading_msg = await message.reply("🤖 **AI Responding...**")
        
        response = await ai_response(message.text or message.reply_to_message.text)
        await loading_msg.edit(response[:Config.MAX_MSG_LENGTH])

# Error handler
@Client.on_message(filters.private)
async def unknown_cmd(client: Client, message: Message):
    if not message.text or message.text.startswith('/'):
        return
    await private_chat(client, message)
