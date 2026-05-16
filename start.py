from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from config import (

    BOT_NAME,

    CHANNEL_LINK,

    DEV_USERNAME

)



def register_start_handlers(app):


    # Start Command

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

                        "📢 Join Channel",

                        url=CHANNEL_LINK

                    )

                ],

                [

                    InlineKeyboardButton(

                        "👨‍💻 Contact Dev",

                        url=f"https://t.me/{DEV_USERNAME.replace('@', '')}"

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

            f"👋 Welcome {message.from_user.mention}\n\n"

            f"🎬 {BOT_NAME}\n\n"

            f"⚡ Advanced Media Processing Bot\n\n"

            f"✅ Thumbnail Support\n"

            f"✅ Metadata Editor\n"

            f"✅ Audio Support\n"

            f"✅ Screenshot Generator\n"

            f"✅ Multi Audio Detection\n"

            f"✅ High GB Support"

        )


        await message.reply_photo(

            photo="assets/welcome.jpg",

            caption=caption,

            reply_markup=buttons

        )



    # Joined Callback

    @app.on_callback_query(

        filters.regex("^joined$")

    )

    async def joined_callback(

        client,

        callback_query

    ):

        await callback_query.answer(

            "✅ Access Granted",

            show_alert=True

        )


        await callback_query.message.reply_text(

            "⚡ You Can Now Use The Bot"

        )