from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from database import users

from metadata import metadata_fields


user_states = {}



def register_metadata_setup(app):


    # Start Setup

    @app.on_message(

        filters.command("set_metadata")

    )

    async def start_metadata_setup(

        client,

        message

    ):

        user_id = message.from_user.id


        data = await users.find_one(

            {"user_id": user_id}

        )


        saved_metadata = {}


        if data and "metadata" in data:

            saved_metadata = data["metadata"]


        user_states[user_id] = {

            "step": 0,

            "data": saved_metadata

        }


        current_field = metadata_fields[0]


        current_value = saved_metadata.get(

            current_field,

            "Not Set"

        )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "⏭ Keep Current",

                        callback_data="keep_metadata"

                    )

                ]

            ]

        )


        await message.reply_text(

            (

                f"🎬 {current_field}\n\n"

                f"Current:\n"

                f"{current_value}\n\n"

                f"Send new value\n"

                f"or press Keep Current"

            ),

            reply_markup=buttons

        )



    # Keep Current Button

    @app.on_callback_query(

        filters.regex("^keep_metadata$")

    )

    async def keep_metadata(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_states:
            return


        user_states[user_id]["step"] += 1


        await next_metadata_step(

            callback_query.message,

            user_id

        )



    # Metadata Collector

    @app.on_message(

        filters.text &

        ~filters.command(

            [

                "start",

                "set_metadata"

            ]

        )

    )

    async def metadata_collector(

        client,

        message

    ):

        user_id = message.from_user.id


        if user_id not in user_states:
            return


        current_step = user_states[user_id]["step"]


        current_field = metadata_fields[current_step]


        user_states[user_id]["data"][current_field] = (

            message.text.strip()

        )


        user_states[user_id]["step"] += 1


        await next_metadata_step(

            message,

            user_id

        )



    # Next Step System

    async def next_metadata_step(

        message,

        user_id

    ):

        current_step = user_states[user_id]["step"]


        total = len(metadata_fields)


        # Finished

        if current_step >= total:


            metadata_data = user_states[user_id]["data"]


            await users.update_one(

                {"user_id": user_id},

                {

                    "$set": {

                        "metadata": metadata_data

                    }

                },

                upsert=True

            )


            del user_states[user_id]


            return await message.reply_text(

                "✅ Metadata Saved Successfully"

            )


        current_field = metadata_fields[current_step]


        current_value = user_states[user_id]["data"].get(

            current_field,

            "Not Set"

        )


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "⏭ Keep Current",

                        callback_data="keep_metadata"

                    )

                ]

            ]

        )


        await message.reply_text(

            (

                f"🎬 {current_field}\n\n"

                f"Current:\n"

                f"{current_value}\n\n"

                f"Send new value\n"

                f"or press Keep Current\n\n"

                f"📊 Step: {current_step + 1}/{total}"

            ),

            reply_markup=buttons

        )