from motor.motor_asyncio import (

    AsyncIOMotorClient

)

from config import MONGO_URI


client = AsyncIOMotorClient(

    MONGO_URI

)


db = client["mediaforge_bot"]


# User Data

users = db["users"]


# Queue System

queue_db = db["queue"]


# Bot Settings

settings_db = db["settings"]


# Statistics

stats_db = db["stats"]


# Temp Cache

cache_db = db["cache"]



async def check_mongo():

    try:

        await client.admin.command(

            "ping"

        )

        return True

    except:
        return False