from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_USERNAME

def require_fsub(func):
    async def wrapper(client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        try:
            member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
            if member.status in ("left", "kicked"):
                raise Exception()
        except:
            return await message.reply_text(
                "<blockquote>ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ɪɴɪ, sɪʟᴀᴋᴀɴ Jᴏɪɴ ᴄʜᴀɴɴᴇʟ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.</blockquote>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Jᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_USERNAME}")]]
                )
            )
        return await func(client, message, *args, **kwargs)
    return wrapper