import os

import uuid

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton,

    InputMediaPhoto

)

from database import users

from cleaner import delete_files

from ffmpeg_tools import (

    process_media,

    get_media_info,

    generate_screenshots,

    detect_audio_languages,

    get_duration

)


os.makedirs(

    "temp",

    exist_ok=True

)



def register_media_handlers(app):


    # Save Cover

    @app.on_message(filters.photo)

    async def save_cover(

        client,

        message

    ):

        user_id = message.from_user.id


        await users.update_one(

            {"user_id": user_id},

            {

                "$set": {

                    "cover_id": message.photo.file_id

                }

            },

            upsert=True

        )


        await message.reply_text(

            "✅ Cover Saved Successfully"

        )



    # Media Detection

    @app.on_message(

        filters.video |

        filters.audio |

        filters.document

    )

    async def media_handler(

        client,

        message

    ):

        media_type = "video"


        if message.audio:

            media_type = "audio"


        buttons = []


        # Audio Buttons

        if media_type == "audio":

            buttons = [

                [

                    InlineKeyboardButton(

                        "📝 Metadata",

                        callback_data=f"metadata_{message.id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "⚡ Process",

                        callback_data=f"both_{message.id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "ℹ Media Info",

                        callback_data=f"info_{message.id}"

                    )

                ]

            ]


        # Video Buttons

        else:

            buttons = [

                [

                    InlineKeyboardButton(

                        "🖼 Thumbnail",

                        callback_data=f"thumbnail_{message.id}"

                    ),

                    InlineKeyboardButton(

                        "📝 Metadata",

                        callback_data=f"metadata_{message.id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "⚡ Both",

                        callback_data=f"both_{message.id}"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "ℹ Media Info",

                        callback_data=f"info_{message.id}"

                    )

                ]

            ]


        processing_message = await message.reply_text(

            "⚡",

            reply_markup=InlineKeyboardMarkup(buttons)

        )


        await processing_message.delete()



    # Thumbnail Check

    @app.on_callback_query(

        filters.regex("^thumbnail_")

    )

    async def thumbnail_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        data = await users.find_one(

            {"user_id": user_id}

        )


        if not data or "cover_id" not in data:


            buttons = InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "⚡ Continue Without Thumbnail",

                            callback_data="continue_without_thumb"

                        )

                    ],

                    [

                        InlineKeyboardButton(

                            "🖼 Set Cover",

                            callback_data="set_cover"

                        )

                    ]

                ]

            )


            return await callback_query.message.reply_text(

                "⚠ Cover Image Not Found",

                reply_markup=buttons

            )


        await callback_query.answer(

            "✅ Cover Found"

        )



    # Metadata Check

    @app.on_callback_query(

        filters.regex("^metadata_")

    )

    async def metadata_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        data = await users.find_one(

            {"user_id": user_id}

        )


        if not data or "metadata" not in data:


            buttons = InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "⚡ Continue Without Metadata",

                            callback_data="continue_without_metadata"

                        )

                    ],

                    [

                        InlineKeyboardButton(

                            "📝 Set Metadata",

                            callback_data="set_metadata"

                        )

                    ]

                ]

            )


            return await callback_query.message.reply_text(

                "⚠ Metadata Not Found",

                reply_markup=buttons

            )


        await callback_query.answer(

            "✅ Metadata Found"

        )



    # Main Processing

    @app.on_callback_query(

        filters.regex("^both_")

    )

    async def both_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        data = await users.find_one(

            {"user_id": user_id}

        )


        await callback_query.answer(

            "⚡ Processing"

        )


        try:

            message_id = int(

                callback_query.data.split("_")[1]

            )

        except:
            return


        original_message = await client.get_messages(

            callback_query.message.chat.id,

            message_id

        )


        unique_id = str(uuid.uuid4())


        input_file = (

            f"temp/{unique_id}_input"

        )


        output_file = (

            f"temp/{unique_id}_output.mkv"

        )


        cover_file = None


        if data and "cover_id" in data:

            cover_file = (

                f"temp/{unique_id}_cover.jpg"

            )


            await client.download_media(

                data["cover_id"],

                file_name=cover_file

            )


        downloaded = await original_message.download(

            file_name=input_file

        )


        metadata = {}


        if data and "metadata" in data:

            metadata = data["metadata"]


        media_info = await get_media_info(

            downloaded

        )


        languages = await detect_audio_languages(

            media_info

        )


        if languages:

            metadata["audio_languages"] = (

                ", ".join(languages)

            )


        await process_media(

            downloaded,

            cover_file,

            output_file,

            metadata

        )


        await callback_query.message.reply_document(

            document=output_file,

            caption="✅ Processing Completed"

        )


        # Screenshots

        if original_message.video:


            screenshot_folder = (

                f"temp/{unique_id}_shots"

            )


            await generate_screenshots(

                output_file,

                screenshot_folder

            )


            screenshots = []


            for file in os.listdir(

                screenshot_folder

            )[:5]:

                screenshots.append(

                    InputMediaPhoto(

                        media=f"{screenshot_folder}/{file}"

                    )

                )


            if screenshots:


                await callback_query.message.reply_text(

                    "📸 Here are some screenshots"

                )


                await callback_query.message.reply_media_group(

                    screenshots

                )


            await delete_files(

                screenshot_folder

            )


        await delete_files(

            downloaded,

            output_file,

            cover_file

        )



    # Continue Buttons

    @app.on_callback_query(

        filters.regex("continue_without_thumb")

    )

    async def continue_without_thumb(

        client,

        callback_query

    ):

        await callback_query.answer(

            "⚡ Continuing"

        )



    @app.on_callback_query(

        filters.regex("continue_without_metadata")

    )

    async def continue_without_metadata(

        client,

        callback_query

    ):

        await callback_query.answer(

            "⚡ Continuing"

        )



    @app.on_callback_query(

        filters.regex("continue_anyway")

    )

    async def continue_anyway(

        client,

        callback_query

    ):

        await callback_query.answer(

            "⚡ Continuing"

        )



    # Set Cover

    @app.on_callback_query(

        filters.regex("set_cover")

    )

    async def set_cover_callback(

        client,

        callback_query

    ):

        await callback_query.message.reply_text(

            "🖼 Send Cover Image"

        )



    # Set Metadata

    @app.on_callback_query(

        filters.regex("set_metadata")

    )

    async def set_metadata_callback(

        client,

        callback_query

    ):

        await callback_query.message.reply_text(

            "📝 Use /set_metadata"

        )



    # Media Info

    @app.on_callback_query(

        filters.regex("^info_")

    )

    async def media_info_callback(

        client,

        callback_query

    ):

        try:

            message_id = int(

                callback_query.data.split("_")[1]

            )

        except:
            return


        original_message = await client.get_messages(

            callback_query.message.chat.id,

            message_id

        )


        unique_id = str(uuid.uuid4())


        temp_file = (

            f"temp/{unique_id}_info"

        )


        downloaded = await original_message.download(

            file_name=temp_file

        )


        media_info = await get_media_info(

            downloaded

        )


        duration = await get_duration(

            media_info

        )


        languages = await detect_audio_languages(

            media_info

        )


        size = round(

            os.path.getsize(downloaded) /

            (1024 * 1024),

            2

        )


        text = (

            f"📦 Size: {size} MB\n"

            f"🕒 Duration: {duration} sec\n"

            f"🎧 Audio: {', '.join(languages) if languages else 'Unknown'}"

        )


        await callback_query.message.reply_text(

            text

        )


        await delete_files(

            downloaded

        )