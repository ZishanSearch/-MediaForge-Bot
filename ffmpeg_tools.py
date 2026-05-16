import os

import json

import subprocess

import shlex



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


    result = subprocess.check_output(

        cmd

    )


    return json.loads(result)



async def process_media(

    input_file,
    cover_file,
    output_file,
    metadata=None

):

    metadata_cmd = ""


    if metadata:

        for key, value in metadata.items():

            if value:

                metadata_cmd += (

                    f'-metadata {key}="{value}" '

                )


    cover_cmd = ""


    if cover_file:

        cover_cmd = (

            f'-i "{cover_file}" '

            f'-map 0 -map 1 '

            f'-disposition:v:1 attached_pic '

        )


    cmd = (

        f'ffmpeg -y '

        f'-i "{input_file}" '

        f'{cover_cmd} '

        f'-c copy '

        f'{metadata_cmd} '

        f'"{output_file}"'

    )


    subprocess.run(

        shlex.split(cmd),

        stdout=subprocess.DEVNULL,

        stderr=subprocess.DEVNULL

    )



async def generate_screenshots(

    video,
    output_folder,
    count=5

):

    os.makedirs(

        output_folder,

        exist_ok=True

    )


    cmd = (

        f'ffmpeg -y '

        f'-i "{video}" '

        f'-vf fps=1/60 '

        f'-q:v 2 '

        f'"{output_folder}/shot_%03d.jpg"'

    )


    subprocess.run(

        shlex.split(cmd),

        stdout=subprocess.DEVNULL,

        stderr=subprocess.DEVNULL

    )



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

                languages.append(

                    lang.upper()

                )


    return list(

        set(languages)

    )



async def get_duration(

    media_info

):

    try:

        duration = float(

            media_info["format"]["duration"]

        )

        return int(duration)

    except:
        return 0



async def clean_filename(

    filename

):

    invalid_chars = [

        "<",
        ">",
        ":",
        '"',
        "/",
        "\\",
        "|",
        "?",
        "*"

    ]


    for char in invalid_chars:

        filename = filename.replace(

            char,

            ""

        )


    return filename.strip()