import os

import shutil

import psutil

import time

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from config import OWNER_ID


START_TIME = time.time()



def register_owner_panel(app):


    @app.on_message(

        filters.command("panel")

    )

    async def owner_panel(

        client,

        message

    ):

        if message.from_user.id != OWNER_ID:

            return await message.reply_text(

                "❌ Unauthorized Access"

            )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "💾 Storage",

                        callback_data="storage"

                    ),

                    InlineKeyboardButton(

                        "🧠 RAM",

                        callback_data="ram"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "⚡ CPU",

                        callback_data="cpu"

                    ),

                    InlineKeyboardButton(

                        "📂 Temp",

                        callback_data="temp"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🧹 Clean Temp",

                        callback_data="clean_temp"

                    )

                ]

            ]

        )


        uptime = int(

            time.time() - START_TIME

        )


        text = (

            f"⚙ Owner Control Panel\n\n"

            f"⏳ Uptime: {uptime} sec\n"

            f"🤖 Bot Status: Online"

        )


        await message.reply_text(

            text,

            reply_markup=buttons

        )



def get_storage():

    total, used, free = shutil.disk_usage("/")


    used_percent = round(

        (used / total) * 100,

        2

    )


    return (

        f"💾 Storage Information\n\n"

        f"Used: {used // (2**30)} GB\n"

        f"Free: {free // (2**30)} GB\n"

        f"Total: {total // (2**30)} GB\n"

        f"Usage: {used_percent}%"

    )



def get_ram():

    ram = psutil.virtual_memory()


    return (

        f"🧠 RAM Information\n\n"

        f"Used: {ram.used // (2**30)} GB\n"

        f"Available: {ram.available // (2**30)} GB\n"

        f"Usage: {ram.percent}%"

    )



def get_cpu():

    cpu = psutil.cpu_percent(interval=1)


    return (

        f"⚡ CPU Usage\n\n"

        f"Usage: {cpu}%"

    )