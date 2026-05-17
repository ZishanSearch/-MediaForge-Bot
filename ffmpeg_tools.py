import os

import json

import asyncio

import subprocess



async def get_media_info(file_path):

    cmd = [

        "ffprobe",

        "-v",

        "quiet",

        "-print_format",

        "json",

        "-show_format",

        "-show_streams",

        file_path

    ]


    result = subprocess.check_output(cmd)


    return json.loads(result)



async def process_media(

    input_file,

    cover_file,

    output_file,

    metadata=None

):

    metadata_cmd = []


    if metadata:

        for key, value in metadata.items():

            if value:

                metadata_cmd.extend(

                    [

                        "-metadata",

                        f"{key}={value}"

                    ]

                )


    cmd = [

        "ffmpeg",

        "-i",

        input_file

    ]


    # Cover

    if cover_file:

        cmd.extend(

            [

                "-i",

                cover_file,

                "-map",

                "0",

                "-map",

                "1",

                "-disposition:v:1",

                "attached_pic"

            ]

        )


    # Fast Stream Copy

    cmd.extend(

        [

            "-c",

            "copy"

        ]

    )


    # Metadata

    cmd.extend(metadata_cmd)


    cmd.extend(

        [

            "-y",

            output_file

        ]

    )


    process = await asyncio.create_subprocess_exec(

        *cmd,

        stdout=asyncio.subprocess.PIPE,

        stderr=asyncio.subprocess.PIPE

    )


    await process.communicate()



async def generate_screenshots(

    video,

    output_folder

):

    os.makedirs(

        output_folder,

        exist_ok=True

    )


    cmd = [

        "ffmpeg",

        "-i",

        video,

        "-vf",

        "fps=1/30",

        f"{output_folder}/shot_%03d.jpg",

        "-y"

    ]


    process = await asyncio.create_subprocess_exec(

        *cmd,

        stdout=asyncio.subprocess.PIPE,

        stderr=asyncio.subprocess.PIPE

    )


    await process.communicate()



async def detect_audio_languages(

    media_info

):

    languages = []


    for stream in media_info.get(

        "streams",

        []

    ):

        if stream.get(

            "codec_type"

        ) == "audio":


            tags = stream.get(

                "tags",

                {}

            )


            lang = tags.get(

                "language"

            )


            if lang:

                languages.append(lang)


    return list(

        set(languages)

    )
