from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from pyrogram.errors import UserNotParticipant

from config import (

    BOT_NAME,

    CHANNEL_LINK,

    DEV_USERNAME

)

from database import users


CHANNEL_USERNAME = "xuluzone"

OTHER_BOT = "https://t.me/Cleanerxulubot"


def register_start_handlers(app):


    # Start Command

    @app.on_message(

        filters.command("start")

    )

    async def start_command(    

        client,

        message

    ):

        user_id = message.from_user.id


        await users.update_one(

            {"user_id": user_id},

            {

                "$set": {

                    "user_id": user_id

                }

            },

            upsert=True

        )

        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🤖 Other Bot",

                        url=OTHER_BOT

                    ),

                    InlineKeyboardButton(

                        "📢 Join Channel",

                        url=CHANNEL_LINK

                    )

                ],

                [

                    InlineKeyboardButton(

                        "✅ Joined",

                        callback_data="joined"

                    )

                ]

            ]

        )


        caption = (

            f"👋 Hello {message.from_user.mention}\n\n"

            f"Welcome to {BOT_NAME}\n\n"

            f"⚡ Advanced media processing bot\n"

            f"with thumbnail editor,\n"

            f"metadata editor,\n"

            f"screenshots,\n"

            f"audio detection\n"

            f"and more.\n\n"

            f"📢 Please join our channel\n"

            f"to continue using the bot."

        )


        await message.reply_photo(

            photo="https://i.postimg.cc/MHp8BbD1/bot-start-banner-2nd.png",

            caption=caption,

            reply_markup=buttons

        )



    # Joined Button

    @app.on_callback_query(

        filters.regex("^joined$")

    )

    async def joined_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        try:

            await client.get_chat_member(

                CHANNEL_USERNAME,

                user_id

            )

        except UserNotParticipant:


            return await callback_query.answer(

                "❌ Please join the channel first.",

                show_alert=True

            )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🖼 Thumbnail",

                        callback_data="thumbnail_help"

                    ),

                    InlineKeyboardButton(

                        "📝 Metadata",

                        callback_data="metadata_help"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📸 Screenshots",

                        callback_data="screenshot_help"

                    ),

                    InlineKeyboardButton(

                        "👨‍💻 Contact Dev",

                        url=f"https://t.me/{DEV_USERNAME.replace('@', '')}"

                    )

                ]

            ]

        )


        caption = (

            f"👋 Hello {callback_query.from_user.mention}\n\n"

            f"Welcome to {BOT_NAME}\n\n"

            f"⚡ Your advanced media editor\n"

            f"is ready to use."

        )


        await callback_query.message.reply_photo(

            photo="https://i.postimg.cc/MHp8BbD1/bot-start-banner-2nd.png",

            caption=caption,

            reply_markup=buttons

        )


        await callback_query.answer(

            "✅ Access Granted"

        )
