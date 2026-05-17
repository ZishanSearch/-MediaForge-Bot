import os

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from database import users


media_store = {}

metadata_editor = {}

global_metadata = {}

global_cover = {}


def media_buttons(media_id):

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "🖼 Set Cover",

                    callback_data=f"setcover_{media_id}"

                ),

                InlineKeyboardButton(

                    "📝 Metadata",

                    callback_data=f"metadata_{media_id}"

                )

            ],

            [

                InlineKeyboardButton(

                    "📸 Screenshots",

                    callback_data=f"screenshotmenu_{media_id}"

                ),

                InlineKeyboardButton(

                    "⚡ Process",

                    callback_data=f"process_{media_id}"

                )

            ],

            [

                InlineKeyboardButton(

                    "ℹ Media Info",

                    callback_data=f"info_{media_id}"

                )

            ]

        ]

    )


def register_media_handlers(app):


    # Save Media

    @app.on_message(

        filters.video |

        filters.document

    )

    async def media_handler(

        client,

        message

    ):

        media_id = message.id


        media_store[media_id] = {

            "message": message,

            "metadata": {},

            "cover": None

        }


        await message.reply_text(

            "⚡ Select Action",

            reply_markup=media_buttons(

                media_id

            )

        )



    # Save Cover Photo

    @app.on_message(filters.photo)

    async def save_cover(

        client,

        message

    ):

        user_id = message.from_user.id


        if user_id not in metadata_editor:

            return


        media_id = metadata_editor[user_id]


        processing = await message.reply_text(

            "⚡"

        )


        photo_path = await message.download(

            file_name=f"temp/{media_id}_cover.jpg"

        )


        media_store[media_id]["cover"] = photo_path


        await processing.delete()


        await message.reply_text(

            "🖼 Cover Saved"

        )



    # Metadata Input

    @app.on_message(

        filters.text &

        ~filters.command([

            "start",

            "broadcast",

            "panel"

        ])

    )

    async def metadata_input(

        client,

        message

    ):

        user_id = message.from_user.id


        if user_id not in metadata_editor:

            return


        data = metadata_editor[user_id]


        media_id = data["media_id"]

        if data["field"] == "cover":

    processing = await message.reply_text(
        "⚡"
    )

    photo_path = await message.download(
        file_name=f"temp/{media_id}_cover.jpg"
    )

    media_store[media_id]["cover"] = photo_path

    del metadata_editor[user_id]

    await processing.delete()

    return await message.reply_text(
        "🖼 Cover Saved"
    )

        field = data["field"]


        media_store[media_id]["metadata"][field] = (

            message.text

        )


        del metadata_editor[user_id]


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "💾 Save For All Files",

                        callback_data=f"saveall_{media_id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📁 Save For This File Only",

                        callback_data=f"savefile_{media_id}"

                    )

                ]

            ]

        )


        await message.reply_text(

            f"✅ {field} Saved",

            reply_markup=buttons

        )
