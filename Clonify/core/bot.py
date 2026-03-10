from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class PRO(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="Clonify",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # --- Send startup message safely ---
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid, ValueError) as ex:
            LOGGER(__name__).warning(
                f"Cannot access log group/channel: {type(ex).__name__}. "
                f"Make sure bot is added and admin. Continuing..."
            )
        except Exception as ex:
            LOGGER(__name__).warning(
                f"Unexpected error sending message to log channel: {type(ex).__name__}. "
                f"Continuing..."
            )

        # --- Check admin status safely ---
        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).warning(
                    "Bot is not admin in log group/channel. Some features may not work."
                )
        except Exception as ex:
            LOGGER(__name__).warning(
                f"Could not verify admin status: {type(ex).__name__}. Some features may fail."
            )

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
