import asyncio

from pyrogram import filters

from pyrogram.errors import FloodWait

from database import users

from config import OWNER_ID


broadcast_state = {}



def register_broadcast_handlers(app):


    # Start Broadcast

    @app.on_message(

        filters.command("broadcast")

    )

    async def start_broadcast(

        client,

        message

    ):

        if message.from_user.id != OWNER_ID:

            return


        broadcast_state[message.from_user.id] = True


        await message.reply_text(

            "📢 Send message to broadcast."

        )



    # Broadcast Handler

    @app.on_message(

        filters.all

    )

    async def handle_broadcast(

        client,

        message

    ):

        user_id = message.from_user.id


        if user_id != OWNER_ID:
            return


        if user_id not in broadcast_state:
            return


        del broadcast_state[user_id]


        all_users = users.find({})


        success = 0

        failed = 0


        progress = await message.reply_text(

            "📡 Broadcasting Started..."

        )


        async for user in all_users:


            target_id = user.get(

                "user_id"

            )


            if not target_id:
                continue


            try:


                # Forwarded Message

                if message.forward_date:


                    await message.forward(

                        chat_id=target_id

                    )


                # Normal Message

                else:


                    await message.copy(

                        chat_id=target_id

                    )


                success += 1


            except FloodWait as e:


                await asyncio.sleep(

                    e.value

                )


            except:

                failed += 1


        await progress.edit_text(

            (

                f"✅ Broadcast Completed\n\n"

                f"Success: {success}\n"

                f"Failed: {failed}"

            )

        )