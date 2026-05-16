import os

import shutil

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from owner_panel import (

    get_storage,

    get_ram,

    get_cpu

)



def register_callback_handlers(app):


    # Storage

    @app.on_callback_query(

        filters.regex("^storage$")

    )

    async def storage_callback(

        client,

        callback_query

    ):

        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🔄 Refresh",

                        callback_data="storage"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🔙 Back",

                        callback_data="owner_panel"

                    )

                ]

            ]

        )


        await callback_query.message.edit_text(

            get_storage(),

            reply_markup=buttons

        )



    # RAM

    @app.on_callback_query(

        filters.regex("^ram$")

    )

    async def ram_callback(

        client,

        callback_query

    ):

        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🔄 Refresh",

                        callback_data="ram"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🔙 Back",

                        callback_data="owner_panel"

                    )

                ]

            ]

        )


        await callback_query.message.edit_text(

            get_ram(),

            reply_markup=buttons

        )



    # CPU

    @app.on_callback_query(

        filters.regex("^cpu$")

    )

    async def cpu_callback(

        client,

        callback_query

    ):

        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🔄 Refresh",

                        callback_data="cpu"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🔙 Back",

                        callback_data="owner_panel"

                    )

                ]

            ]

        )


        await callback_query.message.edit_text(

            get_cpu(),

            reply_markup=buttons

        )



    # Temp Files

    @app.on_callback_query(

        filters.regex("^temp$")

    )

    async def temp_callback(

        client,

        callback_query

    ):

        total_files = 0

        total_size = 0


        for file in os.listdir("temp"):

            file_path = f"temp/{file}"


            if os.path.isfile(file_path):

                total_files += 1

                total_size += os.path.getsize(file_path)


        size_mb = round(

            total_size / (1024 * 1024),

            2

        )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🧹 Clean Temp",

                        callback_data="clean_temp"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🔄 Refresh",

                        callback_data="temp"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "🔙 Back",

                        callback_data="owner_panel"

                    )

                ]

            ]

        )


        await callback_query.message.edit_text(

            (

                f"📂 Temp Information\n\n"

                f"Files: {total_files}\n"

                f"Size: {size_mb} MB"

            ),

            reply_markup=buttons

        )



    # Clean Temp

    @app.on_callback_query(

        filters.regex("^clean_temp$")

    )

    async def clean_temp_callback(

        client,

        callback_query

    ):

        deleted = 0


        for file in os.listdir("temp"):

            file_path = f"temp/{file}"


            try:

                if os.path.isfile(file_path):

                    os.remove(file_path)

                    deleted += 1

            except:
                pass


        await callback_query.message.edit_text(

            (

                f"🧹 Temp Cleaned Successfully\n\n"

                f"Deleted Files: {deleted}"

            )

        )



    # Back To Owner Panel

    @app.on_callback_query(

        filters.regex("^owner_panel$")

    )

    async def owner_panel_callback(

        client,

        callback_query

    ):

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


        await callback_query.message.edit_text(

            "⚙ Owner Control Panel",

            reply_markup=buttons

        )

    @app.on_callback_query(
        filters.regex("thumbnail_help")
    )
    async def thumbnail_help(
        client,
        callback_query
    ):

        await callback_query.answer()

        await callback_query.message.reply_text(

            "🖼 Send image first to save thumbnail."

        )


    @app.on_callback_query(
        filters.regex("metadata_help")
    )
    async def metadata_help(
        client,
        callback_query
    ):

        await callback_query.answer()

        await callback_query.message.reply_text(

            "📝 Use /set_metadata"

        )


    @app.on_callback_query(
        filters.regex("screenshot_help")
    )
    async def screenshot_help(
        client,
        callback_query
    ):

        await callback_query.answer()

        await callback_query.message.reply_text(

            "📸 Send video to generate screenshots."

        )
