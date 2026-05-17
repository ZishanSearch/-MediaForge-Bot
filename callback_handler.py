import os

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton,

    InputMediaPhoto

)

from media import (

    media_store,

    metadata_editor,

    global_metadata,

    global_cover

)

from ffmpeg_tools import (

    process_media,

    generate_screenshots

)

from cleaner import delete_files


def metadata_menu(media_id):

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "🏷 Title",

                    callback_data=f"edit_title_{media_id}"

                ),

                InlineKeyboardButton(

                    "👤 Artist",

                    callback_data=f"edit_artist_{media_id}"

                )

            ],

            [

                InlineKeyboardButton(

                    "📅 Year",

                    callback_data=f"edit_year_{media_id}"

                ),

                InlineKeyboardButton(

                    "⚡ Encoder",

                    callback_data=f"edit_encoder_{media_id}"

                )

            ]

        ]

    )


def screenshot_menu(media_id):

    return InlineKeyboardMarkup(

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


def register_callback_handlers(app):


    # Metadata Menu

    @app.on_callback_query(

        filters.regex("^metadata_")

    )

    async def metadata_callback(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        await callback_query.message.reply_text(

            "📝 Metadata Editor",

            reply_markup=metadata_menu(

                media_id

            )

        )


    # Edit Metadata

    @app.on_callback_query(

        filters.regex("^edit_")

    )

    async def edit_metadata(

        client,

        callback_query

    ):

        parts = callback_query.data.split("_")


        field = parts[1]

        media_id = int(parts[2])


        metadata_editor[
            callback_query.from_user.id
        ] = {
            "media_id": media_id,
            "field": "cover"
        }

            "field": field

        }


        await callback_query.message.reply_text(

            f"✏ Send {field}"

        )


    # Set Cover

    @app.on_callback_query(

        filters.regex("^setcover_")

    )

    async def set_cover(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        metadata_editor[

            callback_query.from_user.id

        ] = media_id


        await callback_query.message.reply_text(

            "🖼 Send Cover Image"

        )


    # Screenshot Menu

    @app.on_callback_query(

        filters.regex("^screenshotmenu_")

    )

    async def screenshot_callback(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        await callback_query.message.reply_text(

            "📸 Select Screenshot Count",

            reply_markup=screenshot_menu(

                media_id

            )

        )


    # Generate Screenshots

    @app.on_callback_query(

        filters.regex("^ss_")

    )

    async def generate_ss(

        client,

        callback_query

    ):

        parts = callback_query.data.split("_")


        count = int(parts[1])

        media_id = int(parts[2])


        processing = await callback_query.message.reply_text(

            "⚡"

        )


        media_message = media_store[media_id]["message"]


        input_file = await media_message.download(

            file_name=f"temp/{media_id}_ss.mkv"

        )


        output_folder = f"temp/{media_id}_shots"


        await generate_screenshots(

            input_file,

            output_folder

        )


        shots = sorted(

            os.listdir(output_folder)

        )[:count]


        media_group = []


        for shot in shots:

            media_group.append(

                InputMediaPhoto(

                    f"{output_folder}/{shot}"

                )

            )


        await callback_query.message.reply_media_group(

            media_group

        )


        await processing.delete()


        for shot in shots:

            await delete_files(

                f"{output_folder}/{shot}"

            )


        await delete_files(

            input_file

        )


    # Save For All

    @app.on_callback_query(

        filters.regex("^saveall_")

    )

    async def save_all(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        global_metadata[

            callback_query.from_user.id

        ] = media_store[media_id]["metadata"]


        global_cover[

            callback_query.from_user.id

        ] = media_store[media_id]["cover"]


        await callback_query.message.reply_text(

            "💾 Saved For All Files"

        )


    # Save For This File

    @app.on_callback_query(

        filters.regex("^savefile_")

    )

    async def save_file(

        client,

        callback_query

    ):

        await callback_query.message.reply_text(

            "📁 Saved For This File Only"

        )


    # Process

    @app.on_callback_query(

        filters.regex("^process_")

    )

    async def process_callback(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        processing = await callback_query.message.reply_text(

            "⚡"

        )


        media_message = media_store[media_id]["message"]


        input_file = await media_message.download(

            file_name=f"temp/{media_id}_input.mkv"

        )


        output_file = f"temp/{media_id}_output.mkv"


        user_id = callback_query.from_user.id


        metadata = media_store[media_id]["metadata"]


        cover = media_store[media_id]["cover"]


        if not metadata:

            metadata = global_metadata.get(

                user_id,

                {}

            )


        if not cover:

            cover = global_cover.get(

                user_id

            )


        await process_media(

            input_file=input_file,

            cover_file=cover,

            output_file=output_file,

            metadata=metadata

        )


        await callback_query.message.reply_document(

            document=output_file,

            thumb=cover,

            caption="✅ Process Completed"

        )


        await processing.delete()


        await delete_files(

            input_file,

            output_file

        )


    # Media Info

    @app.on_callback_query(

        filters.regex("^info_")

    )

    async def info_callback(

        client,

        callback_query

    ):

        media_id = int(

            callback_query.data.split("_")[-1]

        )


        media = (

            media_store[media_id]["message"].video

            or

            media_store[media_id]["message"].document

        )


        size = round(

            media.file_size / (1024**3),

            2

        )


        text = (

            f"📦 Size: {size} GB\n\n"

            f"📁 File:\n"

            f"{media.file_name}"

        )


        await callback_query.message.reply_text(

            text

        )
