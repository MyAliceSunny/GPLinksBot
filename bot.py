import os
import aiohttp
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")

bot = Client(
    "gplink_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply(
        f"👋 Hello {message.chat.first_name}\n\n"
        "Send me any link and I will convert it into a short earning link 💰"
    )

@bot.on_message(filters.regex(r"https?://"))
async def link_handler(bot, message):
    link = message.text
    url = "https://gplinks.in/api"
    params = {"api": API_KEY, "url": link}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if "shortenedUrl" in data:
                    await message.reply(f"🔗 Your short link:\n{data['shortenedUrl']}")
                else:
                    await message.reply("⚠️ Failed to generate link. Try again later.")
    except Exception as e:
        await message.reply("❌ Error occurred while shortening link.")

bot.run()
