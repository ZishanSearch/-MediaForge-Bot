import os

from pyrogram import filters

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

        await callback_query.answer()


        await callback_query.message.edit_text(

            get_storage()

        )



    # RAM

    @app.on_callback_query(

        filters.regex("^ram$")

    )

    async def ram_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        await callback_query.message.edit_text(

            get_ram()

        )



    # CPU

    @app.on_callback_query(

        filters.regex("^cpu$")

    )

    async def cpu_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        await callback_query.message.edit_text(

            get_cpu()

        )



    # Temp Files

    @app.on_callback_query(

        filters.regex("^temp$")

    )

    async def temp_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        temp_files = len(

            os.listdir("temp")

        )


        await callback_query.message.edit_text(

            f"📂 Temp Files: {temp_files}"

        )



    # Clean Temp

    @app.on_callback_query(

        filters.regex("^clean_temp$")

    )

    async def clean_temp_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        for file in os.listdir("temp"):

            try:

                path = f"temp/{file}"


                if os.path.isfile(path):

                    os.remove(path)

            except:

                pass


        await callback_query.message.edit_text(

            "🧹 Temp Cleaned Successfully"

        )



    # Set Cover Button

    @app.on_callback_query(

        filters.regex("^set_cover$")

    )

    async def set_cover_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        await callback_query.message.reply_text(

            "🖼 Send image to save cover"

        )



    # Set Metadata Button

    @app.on_callback_query(

        filters.regex("^set_metadata$")

    )

    async def set_metadata_callback(

        client,

        callback_query

    ):

        await callback_query.answer()


        await callback_query.message.reply_text(

            "📝 Use /set_metadata"

        )
