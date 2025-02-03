# This code has been modified by Safaridev
# Please do not remove this credit
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL, PORT, BIN_CHANNEL, ON_HEROKU
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from utils import temp, check_reset_time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)
import asyncio
import sys
import importlib
import glob
from pathlib import Path
from aiohttp import web
from pyrogram import idle
from SAFARI.template import web_server
from SAFARI.utils import SafariBot
from SAFARI.utils.keepalive import ping_server
from SAFARI.utils.clients import initialize_clients
from plugins.Dev_Feature.Premium import check_expired_premium

ppath = "plugins/*.py"
files = glob.glob(ppath)
SafariBot.start()
loop = asyncio.get_event_loop()


async def start():
    print('\n')
    print('Initalizing Your Bot')
    bot_info = await SafariBot.get_me()
    SafariBot.username = bot_info.username
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("All Files Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    await Media.ensure_indexes()
    me = await SafariBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    SafariBot.username = '@' + me.username
    SafariBot.loop.create_task(check_expired_premium(SafariBot))
    SafariBot.loop.create_task(check_reset_time())
    logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    logging.info(LOG_STR)
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()
    await SafariBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(temp.U_NAME, temp.B_NAME, today, time))

import schedule
from pyrogram import Client

# Initialize the bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def keep_alive():
    try:
        logging.info("Pinging to keep bot active...")
        await app.send_message("me", "Bot is running!")
    except Exception as e:
        logging.error(f"Keep-alive failed: {e}")

# Function to run scheduled tasks in an async loop
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Run every 60 seconds

# Schedule keep-alive every 10 minutes
schedule.every(10).minutes.do(lambda: asyncio.create_task(keep_alive()))

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(run_schedule())  # Start keep-alive scheduler
        loop.run_until_complete(app.start())  # Start bot
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
        
    
#if __name__ == '__main__':
#    try:
  #      loop.run_until_complete(start())
  #  except KeyboardInterrupt:
    ₹    logging.info('Service Stopped Bye 👋')
