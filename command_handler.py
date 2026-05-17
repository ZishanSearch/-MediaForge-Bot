from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)


def register_command_handlers(app):


    # Process Command

    @app.on_message(

        filters.command("process")

    )

    async def process_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        media_id = message.reply_to_message.id


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "⚡ Process",

                        callback_data=f"process_media_{media_id}"

                    )

                ]

            ]

        )


        await message.reply_text(

            "⚡ Ready To Process",

            reply_markup=buttons

        )



    # Screenshots Command

    @app.on_message(

        filters.command("screenshots")

    )

    async def screenshots_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        media_id = message.reply_to_message.id


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "3️⃣",

                        callback_data=f"ss_3_{media_id}"

                    ),

                    InlineKeyboardButton(

                        "5️⃣",

                        callback_data=f"ss_5_{media_id}"

                    ),

                    InlineKeyboardButton(

                        "7️⃣",

                        callback_data=f"ss_7_{media_id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "1️⃣0️⃣",

                        callback_data=f"ss_10_{media_id}"

                    ),

                    InlineKeyboardButton(

                        "1️⃣2️⃣",

                        callback_data=f"ss_12_{media_id}"

                    ),

                    InlineKeyboardButton(

                        "1️⃣5️⃣",

                        callback_data=f"ss_15_{media_id}"

                    )

                ]

            ]

        )


        await message.reply_text(

            "📸 Select Screenshot Count",

            reply_markup=buttons

        )



    # Media Info Command

    @app.on_message(

        filters.command("info")

    )

    async def info_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        media = (

            message.reply_to_message.video

            or

            message.reply_to_message.document

        )


        size = round(

            media.file_size / (1024**3),

            2

        )


        text = (

            f"📦 Size: {size} GB\n\n"

            f"📁 File Name:\n"

            f"{media.file_name}"

        )


        await message.reply_text(

            text

        )



    # Audio Info Command

    @app.on_message(

        filters.command("audio")

    )

    async def audio_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        await message.reply_text(

            "🎵 Use inline Audio Info button"

        )
