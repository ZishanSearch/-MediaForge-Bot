import asyncio


# Main Queue

queue = asyncio.Queue()


# Active Processing Users

processing_users = set()


# Queue Statistics

queue_stats = {

    "total_processed": 0,

    "active_tasks": 0

}



# Add User To Processing

async def add_processing_user(

    user_id

):

    processing_users.add(user_id)



# Remove User

async def remove_processing_user(

    user_id

):

    processing_users.discard(user_id)



# Check User Processing

async def is_processing(

    user_id

):

    return user_id in processing_users



# Queue Add

async def add_to_queue(

    data

):

    await queue.put(data)



# Queue Get

async def get_from_queue():

    return await queue.get()



# Queue Size

async def get_queue_size():

    return queue.qsize()



# Increment Processed

async def increment_processed():

    queue_stats["total_processed"] += 1



# Active Tasks

async def increment_active():

    queue_stats["active_tasks"] += 1



async def decrement_active():

    if queue_stats["active_tasks"] > 0:

        queue_stats["active_tasks"] -= 1