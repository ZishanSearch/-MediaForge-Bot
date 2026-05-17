import os

from pyrogram import Client

from threading import Thread

from web import run_web

from config import (

    API_ID,

    API_HASH,

    BOT_TOKEN

)

from start import register_start_handlers

from owner_panel import register_owner_panel

from callback_handler import register_callback_handlers

from media import register_media_handlers

from broadcast import register_broadcast_handlers

from command_handler import register_command_handlers


# Auto Create Temp Folder

if not os.path.exists("temp"):

    os.makedirs("temp")


app = Client(

    "MediaForgeBot",

    api_id=API_ID,

    api_hash=API_HASH,

    bot_token=BOT_TOKEN,

    workers=50,

    sleep_threshold=30

)


# Register Systems

register_start_handlers(app)

register_owner_panel(app)

register_callback_handlers(app)

register_media_handlers(app)

register_broadcast_handlers(app)

register_command_handlers(app)


# Fake Web Server

Thread(

    target=run_web

).start()


print(

    "🔥 MediaForge Bot Started"

)


app.run()
