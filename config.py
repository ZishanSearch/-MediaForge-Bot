import os


# Telegram API

API_ID = int(

    os.getenv("API_ID", "0")

)

API_HASH = os.getenv(

    "API_HASH",

    ""

)

BOT_TOKEN = os.getenv(

    "BOT_TOKEN",

    ""

)


# MongoDB

MONGO_URI = os.getenv(

    "MONGO_URI",

    ""

)


# Owner

OWNER_ID = int(

    os.getenv("OWNER_ID", "0")

)


# Bot Information

BOT_NAME = (

    "—͟͟͞͞𝐗𝐔 𝐋𝐔 ᥫ᭡ MediaForge Bot"

)

CHANNEL_LINK = (

    "https://t.me/xuluzone"

)

DEV_USERNAME = (

    "@XuLuXuLuu"

)


# Temp Folder

TEMP_FOLDER = "temp"


# Queue System

MAX_ACTIVE_TASKS = 5


# Screenshot Settings

SCREENSHOT_COUNT = 5


# File Size

MAX_FILE_SIZE = 0


# Workers

WORKERS = 50


# Sleep Threshold

SLEEP_THRESHOLD = 30