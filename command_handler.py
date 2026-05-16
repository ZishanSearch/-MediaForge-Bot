from pyrogram import filters

from database import users

from media import media_store

from ffmpeg_tools import (

    generate_screenshots,

    get_media_info,

    detect_audio_languages

)

from cleaner import delete_files

import os

from pyrogram.types import InputMediaPhoto


def register_command_handlers(app):


    # Process Command

    @app.on_message(

        filters.command("process")

    )

    async def process_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        await message.reply_text(

            "⚡"

        )



    # Screenshots Command

    @app.on_message(

        filters.command("screenshots")

    )

    async def screenshots_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        processing = await message.reply_text(

            "⚡"

        )


        media_message = message.reply_to_message


        input_file = await media_message.download(

            file_name=f"temp/{message.id}_cmd_ss.mkv"

        )


        output_folder = f"temp/{message.id}_cmd_shots"


        await generate_screenshots(

            input_file,

            output_folder

        )


        shots = sorted(

            os.listdir(output_folder)

        )[:5]


        media_group = []


        for shot in shots:

            media_group.append(

                InputMediaPhoto(

                    f"{output_folder}/{shot}"

                )

            )


        await message.reply_media_group(

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



    # Audio Info Command

    @app.on_message(

        filters.command("audio")

    )

    async def audio_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        media_message = message.reply_to_message


        input_file = await media_message.download(

            file_name=f"temp/{message.id}_audio.mkv"

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


        await message.reply_text(

            text

        )


        await delete_files(

            input_file

        )



    # Media Info Command

    @app.on_message(

        filters.command("info")

    )

    async def info_command(

        client,

        message

    ):

        if not message.reply_to_message:

            return await message.reply_text(

                "❌ Reply to media"

            )


        media = (

            message.reply_to_message.video

            or

            message.reply_to_message.document

        )


        size = round(

            media.file_size / (1024**3),

            2

        )


        text = (

            f"📦 Size: {size} GB\n\n"

            f"📁 File Name:\n"

            f"{media.file_name}"

        )


        await message.reply_text(

            text

        )



    # Meta Command

    @app.on_message(

        filters.command("meta")

    )

    async def meta_command(

        client,

        message

    ):

        if len(message.command) < 3:

            return await message.reply_text(

                "❌ Example:\n/meta title Solo Leveling"

            )


        field = message.command[1]

        value = " ".join(

            message.command[2:]

        )


        allowed = [

            "title",

            "artist",

            "year",

            "encoder",

            "genre",

            "comment",

            "subtitle"

        ]


        if field not in allowed:

            return await message.reply_text(

                "❌ Invalid metadata field"

            )


        user_id = message.from_user.id


        user_data = await users.find_one(

            {"user_id": user_id}

        ) or {}


        metadata = user_data.get(

            "metadata",

            {}

        )


        metadata[field] = value


        await users.update_one(

            {"user_id": user_id},

            {

                "$set": {

                    "metadata": metadata

                }

            },

            upsert=True

        )


        await message.reply_text(

            f"✅ {field} updated"

        )
