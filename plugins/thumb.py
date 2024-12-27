import re

from pyrogram import filters

from VIPMUSIC import app
from youtubesearchpython.__future__ import VideosSearch


async def gen_infos(url):
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        title = result["title"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return title, thumbnail


def is_url(url):
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.match(regex, url)
    if match:
        return True, match.group(1)
    return False, None


@app.on_message(
    filters.command(["getthumb", "genthumb", "thumb", "thumbnail"], prefixes="/")
)
async def get_thumbnail_command(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ʏᴛ ᴠɪᴅᴇᴏᴜʀʟ ᴀғᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ"
        )
    try:
        a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
        url = message.text.split(" ")[1]
        i, video_id = is_url(url)
        if not i:
            return await a.edit("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ.")

        title, thumb = await gen_infos(url)
        caption = f"<b>[{title}](https://t.me/{app.username}?start=info_{video_id})</b>"
        await message.reply_photo(thumb, caption=caption)
        await a.delete()
    except Exception as e:
        await a.edit(f"ᴀɴ ᴇʀʀᴏʀʀ ᴏᴄᴜʀʀᴇᴅ: {e}")


__HELP__ = """
**ʏᴏᴜᴛᴜʙᴇ ᴛʜᴜᴍʙɴᴀɪʟ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs**

ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴛʜᴜᴍʙɴᴀɪʟ ғʀᴏᴍ ᴀ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ:

- /getthumb <ʏᴏᴜᴛᴜʙᴇ_ᴜʀʟ>: ɢᴇᴛ ᴛʜᴇ ᴛʜᴜᴍʙɴᴀɪʟ ғᴏʀ ᴀ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ.

- /genthumb <ʏᴏᴜᴛᴜʙᴇ_ᴜʀʟ>: sᴀᴍᴇ ᴀs /getthumb.

- /thumb <ʏᴏᴜᴛᴜʙᴇ_ᴜʀʟ>: sᴀᴍᴇ ᴀs /getthumb.

- /thumbnail <ʏᴏᴜᴛᴜʙᴇ_ᴜʀʟ>: sᴀᴍᴇ ᴀs /getthumb.


**ᴇxᴀᴍᴘʟᴇ:**
- `/getthumb https://www.youtube.com/watch?v=Tl4bQBfOtbg`

**ɴᴏᴛᴇ:**
ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴛʜᴜᴍʙɴᴀɪʟ.
"""

__MODULE__ = "🍷 𝐓𖽻𖽪𖽧𖽜 😻"
