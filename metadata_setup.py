from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from database import users


user_states = {}


metadata_fields = [

    "title",

    "artist",

    "year",

    "encoder"

]


field_titles = {

    "title": "🎬 Title",

    "artist": "🎭 Artist",

    "year": "📅 Year",

    "encoder": "⚡ Encoder"

}


def register_metadata_setup(app):


    # Start Metadata Setup

    @app.on_message(

        filters.command("set_metadata")

    )

    async def start_metadata(

        client,

        message

    ):

        user_id = message.from_user.id


        user_data = await users.find_one(

            {"user_id": user_id}

        ) or {}


        metadata = user_data.get(

            "metadata",

            {}

        )


        user_states[user_id] = {

            "step": 0,

            "data": metadata

        }


        field = metadata_fields[0]


        current = metadata.get(

            field,

            "Not Set"

        )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "⏭ Skip",

                        callback_data="skip_metadata"

                    )

                ]

            ]

        )


        await message.reply_text(

            f"{field_titles[field]}\n\n"

            f"Current:\n"

            f"{current}\n\n"

            f"Send new value\n"

            f"or press Skip",

            reply_markup=buttons

        )



    # Metadata Text Input

    @app.on_message(

        filters.text &

        ~filters.command(["start"])

    )

    async def metadata_input(

        client,

        message

    ):

        user_id = message.from_user.id


        if user_id not in user_states:

            return


        state = user_states[user_id]


        step = state["step"]


        field = metadata_fields[step]


        state["data"][field] = message.text


        await next_step(

            message,

            user_id

        )



    # Skip Metadata

    @app.on_callback_query(

        filters.regex("^skip_metadata$")

    )

    async def skip_metadata(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_states:

            return


        await callback_query.answer()


        await next_step(

            callback_query.message,

            user_id

        )



async def next_step(

    message,

    user_id

):

    state = user_states[user_id]


    state["step"] += 1


    if state["step"] >= len(metadata_fields):


        await users.update_one(

            {"user_id": user_id},

            {

                "$set": {

                    "metadata": state["data"]

                }

            },

            upsert=True

        )


        del user_states[user_id]


        return await message.reply_text(

            "✅ Metadata Saved Successfully"

        )


    field = metadata_fields[state["step"]]


    current = state["data"].get(

        field,

        "Not Set"

    )


    buttons = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "⏭ Skip",

                    callback_data="skip_metadata"

                )

            ]

        ]

    )


    await message.reply_text(

        f"{field_titles[field]}\n\n"

        f"Current:\n"

        f"{current}\n\n"

        f"Send new value\n"

        f"or press Skip",

        reply_markup=buttons

    )
