from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from pyrogram.errors import (

    UserNotParticipant

)

from config import (

    BOT_NAME,

    CHANNEL_LINK,

    DEV_USERNAME

)


CHANNEL_USERNAME = "xuluzone"

OTHER_BOT = "https://t.me/Cleanerxulubot"


def register_start_handlers(app):


    @app.on_message(

        filters.command("start")

    )

    async def start_command(

        client,

        message

    ):

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

            f"👋 Hello "

            f"{message.from_user.mention}\n\n"

            f"Welcome to "

            f"{BOT_NAME}\n\n"

            f"⚡ Ultra Fast Media Editor\n"

            f"with metadata,\n"

            f"thumbnails,\n"

            f"screenshots,\n"

            f"and instant processing.\n\n"

            f"📢 Join channel to continue."

        )


        await message.reply_photo(

            photo="https://i.postimg.cc/MHp8BbD1/bot-start-banner-2nd.png",

            caption=caption,

            reply_markup=buttons

        )



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

                "❌ Join channel first",

                show_alert=True

            )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🖼 Set Cover",

                        callback_data="home_cover"

                    ),

                    InlineKeyboardButton(

                        "📝 Metadata",

                        callback_data="home_meta"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📸 Screenshots",

                        callback_data="home_ss"

                    ),

                    InlineKeyboardButton(

                        "⚡ Process",

                        callback_data="home_process"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "👨‍💻 Contact Dev",

                        url=f"https://t.me/{DEV_USERNAME.replace('@', '')}"

                    )

                ]

            ]

        )


        caption = (

            f"👋 Hello "

            f"{callback_query.from_user.mention}\n\n"

            f"{BOT_NAME} "

            f"is ready to use 😎🔥"

        )


        await callback_query.message.reply_photo(

            photo="https://i.postimg.cc/MHp8BbD1/bot-start-banner-2nd.png",

            caption=caption,

            reply_markup=buttons

        )


        await callback_query.answer(

            "✅ Access Granted"

        )
