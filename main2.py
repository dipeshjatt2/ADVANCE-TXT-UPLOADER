# Don't Remove Credit Tg - @Tushar0125
# Ask Doubt on telegram @Tushar0125

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
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

#pwimg = "https://graph.org/file/8add8d382169e326f67e0-3bf38f92e52955e977.jpg"
#ytimg = "https://graph.org/file/3aa806c302ceec62e6264-60ced740281395f68f.jpg"
cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"  

async def show_random_emojis(message):
    emojis = ['🎊', '🔮', '😎', '⚡️', '🚀', '✨', '💥', '🎉', '🥂', '🍾', '🦠', '🤖', '❤️‍🔥', '🕊️', '💃', '🥳','🐅','🦁']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    
# Define the owner's user ID
OWNER_ID = 5203820046

# List of sudo users (initially empty or pre-populated)
SUDO_USERS = [5203820046]

# ✅ Multiple AUTH CHANNELS allowed
AUTH_CHANNELS = [-4818795203]

def is_authorized(user_id: int) -> bool:
    return (
        user_id == OWNER_ID
        or user_id in SUDO_USERS
        or user_id in AUTH_CHANNELS
    )

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

# Sudo command to add/remove sudo users
@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    try:
        args = message.text.split(" ", 2)
        if len(args) < 2:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
            return

        action = args[1].lower()
        target_user_id = int(args[2])

        if action == "add":
            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} added to sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is already in the sudo list.**")
        elif action == "remove":
            if target_user_id == OWNER_ID:
                await message.reply_text("**🚫 The owner cannot be removed from the sudo list.**")
            elif target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} removed from sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is not in the sudo list.**")
        else:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🇮🇳ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ🇮🇳", url="https://t.me/Tushar0125")
        ],
        [
            InlineKeyboardButton("🔔ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ🔔", url="https://t.me/TxtToVideoUpdateChannel")
        ],
        [
            InlineKeyboardButton("🦋ғᴏʟʟᴏᴡ ᴜs🦋", url="https://t.me/TxtToVideoUpdateChannel")                              
        ],           
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://graph.org/file/996d4fc24564509244988-a7d93d020c96973ba8.jpg",
    "https://graph.org/file/96d25730136a3ea7e48de-b0a87a529feb485c8f.jpg",
    "https://graph.org/file/6593f76ddd8c735ae3ce2-ede9fa2df40079b8a0.jpg",
    "https://graph.org/file/a5dcdc33020aa7a488590-79e02b5a397172cc35.jpg",
    "https://graph.org/file/0346106a432049e391181-7560294e8652f9d49d.jpg",
    "https://graph.org/file/ba49ebe9a8e387addbcdc-be34c4cd4432616699.jpg",
    "https://graph.org/file/26f98dec8b3966687051f-557a430bf36b660e24.jpg",
    "https://graph.org/file/2ae78907fa4bbf3160ffa-2d69cd23fa75cb0c3a.jpg",
    "https://graph.org/file/05ef9478729f165809dd7-3df2f053d2842ed098.jpg",
    "https://graph.org/file/b1330861fed21c4d7275c-0f95cca72c531382c1.jpg",
    "https://graph.org/file/0ebb95807047b062e402a-9e670a0821d74e3306.jpg",
    "https://graph.org/file/b4e5cfd4932d154ad6178-7559c5266426c0a399.jpg",
    "https://graph.org/file/44ffab363c1a2647989bc-00e22c1e36a9fd4156.jpg",
    "https://graph.org/file/5f0980969b54bb13f2a8a-a3e131c00c81c19582.jpg",
    "https://graph.org/file/6341c0aa94c803f94cdb5-225b2999a89ff87e39.jpg",
    "https://graph.org/file/90c9f79ec52e08e5a3025-f9b73e9d17f3da5040.jpg",
    "https://graph.org/file/1aaf27a49b6bd81692064-30016c0a382f9ae22b.jpg",
    "https://graph.org/file/702aa31236364e4ebb2be-3f88759834a4b164a0.jpg",
    "https://graph.org/file/d0c6b9f6566a564cd7456-27fb594d26761d3dc0.jpg",
]

@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls) 
    caption = (
        "**ʜᴇʟʟᴏ👋**\n\n"
        "➠ **ɪ ᴀᴍ ᴛxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.**\n"
        "➠ **ғᴏʀ ᴜsᴇ ᴍᴇ sᴇɴᴅ /tushar.\n"
        "➠ **ғᴏʀ ɢᴜɪᴅᴇ sᴇɴᴅ /help."
    )
    await bot.send_photo(
        chat_id=message.chat.id, 
        photo=random_image_url, 
        caption=caption, 
        reply_markup=keyboard
    )
    
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m: Message):
    await m.reply_text("**𝗦𝘁𝗼𝗽𝗽𝗲𝗱**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
    await m.reply_text("🔮Restarted🔮", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized to use this command.")
        return
    
    await m.reply_text(
        "𝗣𝗹𝗲𝗮𝘀𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗧𝗵𝗲 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗙𝗶𝗹𝗲 (.𝘁𝘅𝘁 𝗳𝗼𝗿𝗺𝗮𝘁).",
        quote=True
    )

    try:
        input_message = await client.listen(m.chat.id)

        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        downloaded_path = await input_message.download()

        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.\n\𝗻📂 𝗦𝗮𝘃𝗲𝗱 𝗜𝗻 youtube_cookies.txt."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    try:
        input_message = await bot.listen(message.chat.id)
        if not input_message.document:
            await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
            return

        file_name = input_message.document.file_name.lower()
        uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)
        uploaded_file = await input_message.download(uploaded_file_path)

        await message.reply_text(
            "🔄 **Send your .txt file name, or type 'd' for the default file name.**"
        )

        user_response = await bot.listen(message.chat.id)
        if user_response.text:
            user_response_text = user_response.text.strip().lower()
            final_file_name = file_name if user_response_text == 'd' else user_response_text + '.txt'
        else:
            final_file_name = file_name

        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()

        subjects = {}
        current_subject = None
        for line in content:
            line = line.strip()
            if line and ":" in line:
                title, url = line.split(":", 1)
                title, url = title.strip(), url.strip()

                if title in subjects:
                    subjects[title]["links"].append(url)
                else:
                    subjects[title] = {"links": [url], "topics": []}

                current_subject = title
            elif line.startswith("-") and current_subject:
                subjects[current_subject]["topics"].append(line.strip("- ").strip())

        sorted_subjects = sorted(subjects.items())
        for title, data in sorted_subjects:
            data["topics"].sort()

        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")

        await message.reply_document(
            document=final_file_path,
            caption="📥**𝗘𝗱𝗶𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿**"
        )

    except Exception as e:
        await message.reply_text(f"🚨 **Error**: {str(e)}")
    finally:
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

def sanitize_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_videos_with_ytdlp(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                title = result.get('title', 'Unknown Title')
                videos = {}
                for entry in result['entries']:
                    video_url = entry.get('url', None)
                    video_title = entry.get('title', None)
                    if video_url:
                        videos[video_title if video_title else "Unknown Title"] = video_url
                return title, videos
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return None, None

def save_to_file(videos, name):
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            if title == "Unknown Title":
                file.write(f"{url}\n")
            else:
                file.write(f"{title}: {url}\n")
    return filename

@bot.on_message(filters.command('yt2txt'))
async def ytplaylist_to_txt(client: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.\n\n🫠 This Command is only for owner.**")
        return

    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist Url :**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(
            document=file_name, 
            caption=f"`{title}`\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿"
        )
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")

@bot.on_message(filters.command("userlist") & filters.user(SUDO_USERS))
async def list_users(client: Client, msg: Message):
    if SUDO_USERS:
        users_list = "\n".join([f"User ID : `{user_id}`" for user_id in SUDO_USERS])
        await msg.reply_text(f"SUDO_USERS :\n{users_list}")
    else:
        await msg.reply_text("No sudo users.")

@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg: Message):
    help_text = (
        "`/start` - Start the bot⚡\n\n"
        "`/tushar` - Download and upload files (sudo)🎬\n\n"
        "`/restart` - Restart the bot🔮\n\n" 
        "`/stop` - Stop ongoing process🛑\n\n"
        "`/cookies` - Upload cookies file🍪\n\n"
        "`/e2t` - Edit txt file📝\n\n"
        "`/yt2txt` - Create txt of yt playlist (owner)🗃️\n\n"
        "`/sudo add` - Add user or group or channel (owner)🎊\n\n"
        "`/sudo remove` - Remove user or group or channel (owner)❌\n\n"
        "`/userlist` - List of sudo user or group or channel📜\n\n"
    )
    await msg.reply_text(help_text)

@bot.on_message(filters.command(["tushar"]))
async def upload(bot: Client, m: Message):
    if not is_authorized(m.chat.id):
        await m.reply_text("**🚫You are not authorized to use this bot.**")
        return

    try:
        editable = await m.reply_text("⚡𝗦𝗘𝗡𝗗 𝗧𝗫𝗧 𝗙𝗜𝗟𝗘⚡")
        input_msg = await bot.listen(
            chat_id=m.chat.id,
            filters=filters.document,
            timeout=300
        )
        
        if not input_msg.document or not input_msg.document.file_name.lower().endswith('.txt'):
            await editable.edit("❌ Please send a valid .TXT file")
            return
            
        x = await input_msg.download()
        await input_msg.delete()
        
        with open(x, "r") as f:
            content = f.read().split("\n")
        
        links = []
        pdf_count = img_count = zip_count = video_count = 0
        
        for i in content:
            if "://" in i:
                url_part = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url_part:
                    pdf_count += 1
                elif url_part.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url_part:
                    zip_count += 1
                else:
                    video_count += 1
        
        os.remove(x)
        
        try:
            await editable.edit(
                f"**Total Links Found: {len(links)}**\n\n"
                f"📷 Images: {img_count}\n"
                f"📄 PDFs: {pdf_count}\n"
                f"🗜 Zips: {zip_count}\n"
                f"🎥 Videos: {video_count}\n\n"
                f"**Send starting index (default: 1)**"
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            editable = await m.reply_text(
                f"**Total Links Found: {len(links)}**\n\n"
                f"📷 Images: {img_count}\n"
                f"📄 PDFs: {pdf_count}\n"
                f"🗜 Zips: {zip_count}\n"
                f"🎥 Videos: {video_count}\n\n"
                f"**Send starting index (default: 1)**"
            )
        
        try:
            index_msg = await bot.listen(chat_id=m.chat.id, filters=filters.text, timeout=120)
            arg = int(index_msg.text) if index_msg.text.isdigit() else 1
            await index_msg.delete()
        except asyncio.TimeoutError:
            arg = 1
        
        await editable.edit("📚 **Enter Batch Name**\n\nSend '1' to use filename")
        batch_msg = await bot.listen(chat_id=m.chat.id, filters=filters.text, timeout=120)
        b_name = input_msg.document.file_name if batch_msg.text == '1' else batch_msg.text
        await batch_msg.delete()
        
        await editable.edit("**📸 Select Resolution**\n\n144 | 240 | 360 | 480 | 720 | 1080")
        res_msg = await bot.listen(chat_id=m.chat.id, filters=filters.text, timeout=120)
        res_text = res_msg.text
        resolution_map = {
            "144": "256x144",
            "240": "426x240",
            "360": "640x360",
            "480": "854x480", 
            "720": "1280x720",
            "1080": "1920x1080"
        }
        res = resolution_map.get(res_text, "UN")
        await res_msg.delete()
        
        await editable.edit("📛 **Enter Your Name**\n\nFormat: Name,Link\nOr send '1' for default")
        credit_msg = await bot.listen(chat_id=m.chat.id, filters=filters.text, timeout=120)
        if credit_msg.text == '1':
            CR = '[𝗧𝘂𝘀𝗵𝗮𝗿](https://t.me/Tushar0125)'
        else:
            try:
                text, link = credit_msg.text.split(',')
                CR = f'[{text.strip()}]({link.strip()})'
            except:
                CR = credit_msg.text
        await credit_msg.delete()
        
        await editable.edit("**🖼️ Send Thumbnail URL**\n\nOr send 'no' for no thumbnail")
        thumb_msg = await bot.listen(chat_id=m.chat.id, filters=filters.text, timeout=120)
        thumb = thumb_msg.text if thumb_msg.text.lower() != "no" else None
        await thumb_msg.delete()
        
        try:
            await editable.delete()
        except:
            pass
        except:
            pass
            
        processing_msg = await m.reply_text("🔄 **Starting Download Process...**")
        
        failed_count = 0
        count = arg if arg > 1 else 1
        
        for i in range(count - 1, len(links)):
            try:
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                url = "https://" + V

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html'}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                
                elif 'media-cdn.classplusapp.com/drm/' in url:
                    url = f"https://dragoapi.vercel.app/video/{url}"
                
                elif 'videos.classplusapp' in url:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "media-cdn.classplusapp" in url:
                    headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                    params = (('url', f'{url}'),)
                    response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                    url = response.json()['url']

                elif "https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/" in url:
                    url = url.replace("https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/", "")
                    name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                    name = f'{str(count).zfill(3)}) {name1[:60]}'
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                    
                elif "https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/" in url:
                    url = url.replace("https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/", "")
                    name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                    name = f'{str(count).zfill(3)}) {name1[:60]}'
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

                elif "apps-s3-jw-prod.utkarshapp.com" in url:
                    if 'enc_plain_mp4' in url:
                        url = url.replace(url.split("/")[-1], res+'.mp4')
                        
                    elif 'Key-Pair-Id' in url:
                        url = None
                        
                    elif '.m3u8' in url:
                        q = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).split("/")[0]
                        x = url.split("/")[5]
                        x = url.replace(x, "")
                        url = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).replace(q+"/", x)

                elif "/master.mpd" in url or "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                    id =  url.split("/")[-2]
                    url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={raw_text4}"
            
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'

                if 'khansirvod4.pc.cdn.bitgravity.com' in url:               
                    parts = url.split('/')               
                    part1 = parts[1]
                    part2 = parts[2]
                    part3 = parts[3] 
                    part4 = parts[4]
                    part5 = parts[5]
                    
                    print(f"PART1: {part1}")
                    print(f"PART2: {part2}")
                    print(f"PART3: {part3}")
                    print(f"PART4: {part4}")
                    print(f"PART5: {part5}")
                    url = f"https://kgs-v4.akamaized.net/kgs-cv/{part3}/{part4}/{part5}"
               
                if "youtu" in url:
                    ytf = f"b[height<={res_text}][ext=mp4]/bv[height<={res_text}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                else:
                    ytf = f"b[height<={res_text}]/bv[height<={res_text}]+ba/b/bv+ba"
              
                if "edge.api.brightcove.com" in url:
                    bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzUxMzUzNjIsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiYmt3cmVIWmxZMFUwVXpkSmJYUkxVemw2ZW5Oclp6MDkiLCJmaXJzdF9uYW1lIjoiY25GdVpVdG5kRzR4U25sWVNGTjRiVW94VFhaUVVUMDkiLCJlbWFpbCI6ImFFWllPRXhKYVc1NWQyTlFTazk0YmtWWWJISTNRM3BKZW1OUVdIWXJWWE0wWldFNVIzZFNLelE0ZHowPSIsInBob25lIjoiZFhSNlFrSm9XVlpCYkN0clRUWTFOR3REU3pKTVVUMDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJhVVZGZGpBMk9XSnhlbXRZWm14amF6TTBVazQxUVQwOSIsImRldmljZV90eXBlIjoid2ViIiwiZGV2aWNlX3ZlcnNpb24iOiJDaHJvbWUrMTE5IiwiZGV2aWNlX21vZGVsIjoiY2hyb21lIiwicmVtb3RlX2FkZHIiOiIyNDA5OjQwYzI6MjA1NTo5MGQ0OjYzYmM6YTNjOTozMzBiOmIxOTkifX0.Kifitj1wCe_ohkdclvUt7WGuVBsQFiz7eezXoF1RduDJi4X7egejZlLZ0GCZmEKBwQpMJLvrdbAFIRniZoeAxL4FZ-pqIoYhH3PgZU6gWzKz5pdOCWfifnIzT5b3rzhDuG7sstfNiuNk9f-HMBievswEIPUC_ElazXdZPPt1gQqP7TmVg2Hjj6-JBcG7YPSqa6CUoXNDHpjWxK_KREnjWLM7vQ6J3vF1b7z_S3_CFti167C6UK5qb_turLnOUQzWzcwEaPGB3WXO0DAri6651WF33vzuzeclrcaQcMjum8n7VQ0Cl3fqypjaWD30btHQsu5j8j3pySWUlbyPVDOk-g'
                    url = url.split("bcov_auth")[0]+bcov
                
                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                
                elif "webvideos.classplusapp." in url:
                    cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
              
                elif "youtube.com" in url or "youtu.be" in url:
                    cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
              
                else:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

                try:  
                    cc = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mkv\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cpvod = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mkv\n\n\n🔗𝗩𝗶𝗱𝗲𝗼 𝗨𝗿𝗹 ➤ <a href="{url}">__Click Here to Watch Video__</a>\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cimg = f'**[📁] 𝗜𝗺𝗴_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.jpg\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cczip = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.zip\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                    cc1 = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.pdf\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
              
                    if "drive" in url:
                        try:
                            ka = await helper.download(url, name)
                            copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                            count+=1
                            os.remove(ka)
                            time.sleep(1)
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue

                    elif ".pdf" in url:
                        try:
                            await asyncio.sleep(4)
                            url = url.replace(" ", "%20")
                            scraper = cloudscraper.create_scraper()
                            response = scraper.get(url)

                            if response.status_code == 200:
                                with open(f'{name}.pdf', 'wb') as file:
                                    file.write(response.content)

                                await asyncio.sleep(4)
                                copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                                count += 1
                                os.remove(f'{name}.pdf')
                            else:
                                await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                            
                    elif "media-cdn.classplusapp.com/drm/" in url:
                        try:
                            await bot.send_photo(chat_id=m.chat.id, photo=cpimg, caption=cpvod)
                            count +=1
                        except Exception as e:
                            await m.reply_text(str(e))    
                            time.sleep(1)    
                            continue          
                            
                    elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png"]):
                        try:
                            await asyncio.sleep(4)
                            url = url.replace(" ", "%20")
                            scraper = cloudscraper.create_scraper()
                            response = scraper.get(url)

                            if response.status_code == 200:
                                with open(f'{name}.jpg', 'wb') as file:
                                    file.write(response.content)

                                await asyncio.sleep(2)
                                copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.jpg', caption=cimg)
                                count += 1
                                os.remove(f'{name}.jpg')
                            else:
                                await m.reply_text(f"Failed to download Image: {response.status_code} {response.reason}")

                        except FloodWait as e:
                            await m.reply_text(str(e))
                            await asyncio.sleep(2)
                            return  
                        
                        except Exception as e:
                            await m.reply_text(f"An error occurred: {str(e)}")
                            await asyncio.sleep(4)
                            
                    elif ".zip" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.zip" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.zip', caption=cczip)
                            count += 1
                            os.remove(f'{name}.zip')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            count += 1
                            continue
                            
                    elif ".pdf" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                    else:
                        emoji_message = await show_random_emojis(message)
                        remaining_links = len(links) - count
                        Show = f"**🍁 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗜𝗡𝗚 🍁**\n\n**📝ɴᴀᴍᴇ » ** `{name}\n\n🔗ᴛᴏᴛᴀʟ ᴜʀʟ » {len(links)}\n\n🗂️ɪɴᴅᴇx » {str(count)}/{len(links)}\n\n🌐ʀᴇᴍᴀɪɴɪɴɢ ᴜʀʟ » {remaining_links}\n\n❄ǫᴜᴀʟɪᴛʏ » {res}`\n\n**🔗ᴜʀʟ » ** `{url}`\n\n🤖𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 ➤ 𝗧𝗨𝗦𝗛𝗔𝗥\n\n🙂 चलो फिर से अजनबी बन जायें 🙂"
                        prog = await m.reply_text(Show)
                        res_file = await helper.download_video(url, cmd, name)
                        filename = res_file
                        await prog.delete(True)
                        await emoji_message.delete()
                        await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                        count += 1
                        time.sleep(1)

                except Exception as e:
                    await m.reply_text(f'‼️𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗙𝗮𝗶𝗹𝗲𝗱‼️\n\n'
                                       f'📝𝗡𝗮𝗺𝗲 » `{name}`\n\n'
                                       f'🔗𝗨𝗿𝗹 » <a href="{url}">__**Click Here to See Link**__</a>`')
                                       
                    count += 1
                    failed_count += 1
                    continue   
                
        await processing_msg.delete()
        await m.reply_text(f"`✨𝗕𝗔𝗧𝗖𝗛 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"📛𝗜𝗻𝗱𝗲𝘅 𝗥𝗮𝗻𝗴𝗲 » ({raw_text} to {len(links)})\n"
                           f"📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 » {b_name}\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"✨𝗧𝗫𝗧 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨ : {len(links)}\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"🔹𝗩𝗶𝗱𝗲𝗼 » {video_count}\n🔹𝗣𝗱𝗳 » {pdf_count}\n🔹𝗜𝗺𝗴 » {img_count}\n🔹𝗭𝗶𝗽 » {zip_count}\n🔹𝗙𝗮𝗶𝗹𝗲𝗱 𝗨𝗿𝗹 » {failed_count}\n\n"
                           f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                           f"✅𝗦𝗧𝗔𝗧𝗨𝗦 » 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗`")
        await m.reply_text(f"<pre><code>📥𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤『{CR}』</code></pre>")
        await m.reply_text(f"<pre><code>『😏𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗞𝗼𝗻 𝗗𝗲𝗴𝗮😏』</code></pre>")                 

    except asyncio.TimeoutError:
        await m.reply_text("⌛ Operation timed out")
    except Exception as e:
        await m.reply_text(f"⚠️ Critical Error: {str(e)}")
    finally:
        if 'x' in locals() and os.path.exists(x):
            os.remove(x)
        if 'thumb' in locals() and thumb and os.path.exists(thumb):
            os.remove(thumb)

if __name__ == "__main__":
    bot.run()
