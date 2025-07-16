#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Don't Remove Credit @Tushar0125
# Ask Doubt on Telegram @Tushar0125

import os
import re
import sys
import json
import time
import m3u8
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import datetime
import random
import ffmpeg
import logging
import yt_dlp
from subprocess import getstatusoutput
from aiohttp import web
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

# ===== CONFIGURATION =====
API_ID = 22118129  # Replace with your API_ID
API_HASH = "43c66e3314921552d9330a4b05b18800"  # Replace with your API_HASH
BOT_TOKEN = "7485383982:AAFuRY-6wQjfHzAloZLRJyYPi9Jp_TzYNR4"  # Replace with your bot token
OWNER_ID = 5203820046  # Your Telegram ID
SUDO_USERS = [5203820046]  # List of sudo users
AUTH_CHANNELS = [-4818795203]  # Authorized channels
COOKIES_FILE = "youtube_cookies.txt"
UPLOAD_FOLDER = "downloads"
THUMBNAIL = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===== HELPER FUNCTIONS =====
def sanitize_filename(name):
    """Remove invalid characters from filenames"""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def is_authorized(user_id: int) -> bool:
    """Check if user is authorized"""
    return (user_id == OWNER_ID or 
            user_id in SUDO_USERS or 
            user_id in AUTH_CHANNELS)

async def download_file(url, filename):
    """Download file with progress"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                async for chunk in response.content.iter_chunked(1024):
                    f.write(chunk)

async def upload_with_progress(client, message, file_path, caption):
    """Upload file with progress indicator"""
    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption=caption,
            progress=progress_bar,
            progress_args=(message, "Uploading...")
        )
        return True
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return False

# ===== BOT INITIALIZATION =====
app = Client(
    "TxtToVideoBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== COMMAND HANDLERS =====
@app.on_message(filters.command("start"))
async def start(client, message):
    """Start command handler"""
    buttons = [
        [InlineKeyboardButton("Developer", url="https://t.me/Tushar0125")],
        [InlineKeyboardButton("Updates", url="https://t.me/TxtToVideoUpdateChannel")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_photo(
        photo=THUMBNAIL,
        caption="**Hello! I'm TXT to Video Uploader Bot**\n\n"
                "Send me a TXT file with links and I'll process them!\n"
                "Use /help to see available commands.",
        reply_markup=reply_markup
    )

@app.on_message(filters.command("help"))
async def help(client, message):
    """Help command handler"""
    help_text = """
📚 **Available Commands:**

🔹 /start - Start the bot
🔹 /help - Show this help message
🔹 /tushar - Process TXT file (sudo only)
🔹 /cookies - Upload cookies file
🔹 /yt2txt - Convert YouTube playlist to TXT (owner only)
🔹 /restart - Restart bot (owner only)
🔹 /stop - Stop current process
🔹 /sudo - Manage sudo users (owner only)
"""
    await message.reply_text(help_text)

@app.on_message(filters.command("tushar") & filters.private)
async def process_txt(client, message):
    """Main processing command"""
    if not is_authorized(message.from_user.id):
        await message.reply_text("🚫 You are not authorized to use this command!")
        return

    # Step 1: Get TXT file
    await message.reply_text("📤 Please send me the TXT file containing links")
    txt_msg = await client.listen(message.chat.id)
    
    if not txt_msg.document or not txt_msg.document.file_name.endswith('.txt'):
        await message.reply_text("❌ Please send a valid TXT file!")
        return

    # Download TXT file
    txt_path = await txt_msg.download()
    
    # Step 2: Get batch name
    await message.reply_text("📝 Enter batch name (or send '1' for default):")
    batch_msg = await client.listen(message.chat.id)
    batch_name = txt_msg.document.file_name if batch_msg.text == '1' else batch_msg.text
    
    # Step 3: Process links
    with open(txt_path, 'r') as f:
        links = [line.strip() for line in f if line.strip()]
    
    os.remove(txt_path)
    
    # Step 4: Process each link
    success = 0
    failed = 0
    
    for i, link in enumerate(links, 1):
        try:
            # Download processing
            await message.reply_text(f"⏳ Processing {i}/{len(links)}: {link[:50]}...")
            
            # Your download logic here
            # Example: yt-dlp or direct download
            
            # Upload processing
            filename = f"{batch_name}_{i}.mp4"
            caption = f"📹 {batch_name}\n\n🔗 {link}\n\n⚡ Downloaded via @TxtToVideoBot"
            
            # Simulate upload
            await asyncio.sleep(2)
            await message.reply_document(
                document="example.mp4",  # Replace with actual file
                caption=caption
            )
            success += 1
            
        except Exception as e:
            logger.error(f"Failed to process {link}: {e}")
            failed += 1
            continue
    
    # Final report
    await message.reply_text(
        f"✅ Process completed!\n\n"
        f"📊 Stats:\n"
        f"• Total links: {len(links)}\n"
        f"• Success: {success}\n"
        f"• Failed: {failed}"
    )

# ===== ADMIN COMMANDS =====
@app.on_message(filters.command("sudo") & filters.user(OWNER_ID))
async def sudo(client, message):
    """Manage sudo users"""
    args = message.text.split()
    if len(args) < 3:
        return await message.reply_text("Usage: /sudo [add/remove] [user_id]")

    action = args[1].lower()
    try:
        user_id = int(args[2])
    except ValueError:
        return await message.reply_text("Invalid user ID!")

    if action == "add":
        if user_id not in SUDO_USERS:
            SUDO_USERS.append(user_id)
            await message.reply_text(f"✅ Added {user_id} to sudo list!")
        else:
            await message.reply_text(f"ℹ️ {user_id} is already sudo!")
    elif action == "remove":
        if user_id in SUDO_USERS:
            SUDO_USERS.remove(user_id)
            await message.reply_text(f"✅ Removed {user_id} from sudo list!")
        else:
            await message.reply_text(f"ℹ️ {user_id} is not in sudo list!")
    else:
        await message.reply_text("Invalid action! Use 'add' or 'remove'")

# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    # Create upload folder if not exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    logger.info("Starting bot...")
    app.run()
    logger.info("Bot stopped")
