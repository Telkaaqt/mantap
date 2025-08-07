import os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from ChampuMusic import app
from ChampuMusic.misc import SUDOERS
from pyrogram.enums import ChatMemberStatus
import asyncio




@app.on_message(filters.command("leave") & SUDOERS)
async def leave(_, message):
    if len(message.command) != 2:
        return await message.reply_text("<blockquote>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɢʀᴏᴜᴘ ɪᴅ. ᴜsᴇ ʟɪᴋᴇ: /leave chat_id.</blockquote>")
    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text(f"<blockquote>ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ɴᴜᴍᴇʀɪᴄ ɪᴅ.</blockquote>")
    CHAMPU = await message.reply_text(f"<blockquote>ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛ... {app.me.mention}</blockquote>")
    try:
        await app.send_message(chat_id, f"<blockquote>{app.me.mention} ʟᴇғᴛɪɴɢ ᴄʜᴀᴛ ʙʏᴇ...</blockquote>")
        await app.leave_chat(chat_id)
        await CHAMPU.edit(f"<blockquote>{app.me.mention} ʟᴇғᴛ ᴄʜᴀᴛ {chat_id}.</blockquote>")
    except Exception as e:
        pass


# Command handler for /givelink command
@app.on_message(filters.command("givelink"))
async def give_link_command(client, message):
    # Generate an invite link for the chat where the command is used
    chat = message.chat.id
    link = await app.export_chat_invite_link(chat)
    await message.reply_text(f"<blockquote>ʜᴇʀᴇ's ᴛʜᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ:\n{link}</blockquote>")


@app.on_message(
    filters.command(
        ["link", "invitelink"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
    & SUDOERS
)
async def link_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ. ᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ: /link group_id")
        return

    group_id = message.command[1]
    file_name = f"group_info_{group_id}.txt"

    try:
        chat = await client.get_chat(int(group_id))

        if chat is None:
            await message.reply("<blockquote>ᴜɴᴀʙʟᴇ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғᴏʀ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ɢʀᴏᴜᴘ ɪᴅ.</blockquote>")
            return

        try:
            invite_link = await client.export_chat_invite_link(chat.id)
        except FloodWait as e:
            await message.reply(f"<blockquote>ғʟᴏᴏᴅᴡᴀɪᴛ: {e.x} sᴇᴄᴏɴᴅs. ʀᴇᴛʀʏɪɴɢ ɪɴ {e.x} sᴇᴄᴏɴᴅs.</blockquote>")
            return

        group_data = {
            "ɪᴅ": chat.id,
            "ᴛʏᴘᴇ": str(chat.type),
            "ᴛɪᴛʟᴇ": chat.title,
            "ᴍᴇᴍʙᴇʀs_ᴄᴏᴜɴᴛ": chat.members_count,
            "ᴅᴇsᴄʀɪᴘᴛɪᴏɴ": chat.description,
            "ɪɴᴠɪᴛᴇ_ʟɪɴᴋ": invite_link,
            "ɪs_ᴠᴇʀɪғɪᴇᴅ": chat.is_verified,
            "ɪs_ʀᴇsᴛʀɪᴄᴛᴇᴅ": chat.is_restricted,
            "ɪs_ᴄʀᴇᴀᴛᴏʀ": chat.is_creator,
            "ɪs_sᴄᴀᴍ": chat.is_scam,
            "ɪs_ғᴀᴋᴇ": chat.is_fake,
            "ᴅᴄ_ɪᴅ": chat.dc_id,
            "ʜᴀs_ᴘʀᴏᴛᴇᴄᴛᴇᴅ_ᴄᴏɴᴛᴇɴᴛ": chat.has_protected_content,
        }

        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")

        await client.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=f"<blockquote expandable>ʜᴇʀᴇ ɪs ᴛʜᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғᴏʀ\n{chat.title}\nᴛʜᴇ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ sᴄʀᴀᴘᴇᴅ ʙʏ : @{app.username}</blockquote>",
        )

    except Exception as e:
        await message.reply(f"Error: {str(e)}")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


__MODULE__ = "Gʀᴏᴜᴘ Lɪɴᴋ"
__HELP__ = """
<blockquote expandable>
<u>- `/givelink`</u>
Gᴇᴛ ᴛʜᴇ ɪɴᴠɪᴛᴇ ɪɴᴋ ғᴏʀ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ.

<u>- `/link ɢʀᴏᴜᴘ_ɪᴅ`</u>
Gᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ɪɴᴠɪᴛᴇ ɪɴᴋ ғᴏʀ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ɢʀᴏᴜᴘ ID.<blockquote>
"""
