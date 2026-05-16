import os

import asyncio

from pyrogram import filters

from pyrogram.types import (

    InlineKeyboardMarkup,

    InlineKeyboardButton

)

from database import users

from ffmpeg_tools import (

    process_media,

    generate_screenshots,

    get_media_info,

    detect_audio_languages

)

from cleaner import delete_files


user_files = {}


def register_media_handlers(app):


    # Save Cover

    @app.on_message(filters.photo)

    async def save_cover(

        client,

        message

    ):

        user_id = message.from_user.id


        processing = await message.reply_text(

            "⚡"

        )


        photo_path = await message.download(

            file_name=f"temp/{user_id}_cover.jpg"

        )


        await users.update_one(

            {"user_id": user_id},

            {

                "$set": {

                    "cover": photo_path

                }

            },

            upsert=True

        )


        await processing.delete()


        await message.reply_text(

            "🖼 Cover Saved Successfully"

        )



    # Video Handler

    @app.on_message(

        filters.video |

        filters.document

    )

    async def video_handler(

        client,

        message

    ):

        user_id = message.from_user.id


        user_files[user_id] = message


        buttons = InlineKeyboardMarkup(

            [

                [

                    InlineKeyboardButton(

                        "🖼 Set Cover",

                        callback_data="set_cover"

                    ),

                    InlineKeyboardButton(

                        "📝 Set Metadata",

                        callback_data="set_metadata"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "📸 Screenshots",

                        callback_data="screenshots"

                    ),

                    InlineKeyboardButton(

                        "🎵 Audio Info",

                        callback_data="audio_info"

                    )

                ],

                [

                    InlineKeyboardButton(

                        "⚡ Process",

                        callback_data="process_media"

                    ),

                    InlineKeyboardButton(

                        "ℹ Media Info",

                        callback_data="media_info"

                    )

                ]

            ]

        )


        await message.reply_text(

            "⚡ Select Action",

            reply_markup=buttons

        )



    # Process Media

    @app.on_callback_query(

        filters.regex("process_media")

    )

    async def process_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_files:

            return await callback_query.answer(

                "❌ Send media first",

                show_alert=True

            )


        processing = await callback_query.message.reply_text(

            "⚡"

        )


        media_message = user_files[user_id]


        input_file = await media_message.download(

            file_name=f"temp/{user_id}_input.mkv"

        )


        output_file = f"temp/{user_id}_output.mkv"


        user_data = await users.find_one(

            {"user_id": user_id}

        ) or {}


        metadata = user_data.get(

            "metadata",

            {}

        )


        cover_path = user_data.get(

            "cover"

        )


        await process_media(

            input_file=input_file,

            cover_file=cover_path,

            output_file=output_file,

            metadata=metadata

        )


        await callback_query.message.reply_document(

            document=output_file,

            thumb=cover_path,

            caption="✅ Processing Completed"

        )


        await processing.delete()


        await delete_files(

            input_file,

            output_file

        )



    # Screenshots

    @app.on_callback_query(

        filters.regex("screenshots")

    )

    async def screenshots_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_files:

            return await callback_query.answer(

                "❌ Send media first",

                show_alert=True

            )


        processing = await callback_query.message.reply_text(

            "⚡"

        )


        media_message = user_files[user_id]


        input_file = await media_message.download(

            file_name=f"temp/{user_id}_ss.mkv"

        )


        output_folder = f"temp/{user_id}_shots"


        await generate_screenshots(

            input_file,

            output_folder

        )


        shots = sorted(

            os.listdir(output_folder)

        )[:5]


        media_group = []


        from pyrogram.types import InputMediaPhoto


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



    # Audio Info

    @app.on_callback_query(

        filters.regex("audio_info")

    )

    async def audio_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_files:

            return await callback_query.answer(

                "❌ Send media first",

                show_alert=True

            )


        media_message = user_files[user_id]


        input_file = await media_message.download(

            file_name=f"temp/{user_id}_audio.mkv"

        )


        media_info = await get_media_info(

            input_file

        )


        languages = await detect_audio_languages(

            media_info

        )


        if not languages:

            text = (

                "⚡ No audio language detected"

            )

        else:

            text = (

                "🎵 Audio Languages\n\n"

                + "\n".join(

                    f"• {lang}"

                    for lang in languages

                )

            )


        await callback_query.message.reply_text(

            text

        )


        await delete_files(

            input_file

        )



    # Media Info

    @app.on_callback_query(

        filters.regex("media_info")

    )

    async def media_info_callback(

        client,

        callback_query

    ):

        user_id = callback_query.from_user.id


        if user_id not in user_files:

            return await callback_query.answer(

                "❌ Send media first",

                show_alert=True

            )


        media_message = user_files[user_id]


        media = media_message.video or media_message.document


        size = round(

            media.file_size / (1024**3),

            2

        )


        text = (

            f"📦 Size: {size} GB\n\n"

            f"📁 File Name:\n"

            f"{media.file_name}"

        )


        await callback_query.message.reply_text(

            text

        )
