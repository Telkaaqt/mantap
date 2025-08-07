import asyncio

import speedtest
from pyrogram import filters

from strings import get_command
from ChampuMusic import app
from ChampuMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("<blockquote>⇆ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...</blockquote>")
        test.download()
        m = m.edit("<blockquote>⇆ ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅᴛᴇsᴛ...</blockquote>")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("<blockquote>↻ sʜᴀʀɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛ</blockquote>")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("<blockquote>ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ</blockquote>")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""<blockquote expandable>**sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛ**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪsᴘ :** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ :** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ :**</u>
**ɴᴀᴍᴇ :** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ :** {result['server']['country']}, {result['server']['cc']}
**sᴘᴏɴsᴏʀ :** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ :** {result['server']['latency']}  
**ᴘɪɴɢ :** {result['ping']}</blockquote>"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
