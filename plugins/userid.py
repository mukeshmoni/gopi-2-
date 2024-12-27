from pyrogram import filters
from pyrogram.enums import ParseMode

from VIPMUSIC import app


@app.on_message(filters.command("me"))
def ids(_, message):
    reply = message.reply_to_message
    if reply:
        message.reply_text(
            f"ʏᴏᴜʀ ɪᴅ: {message.from_user.id}\n{reply.from_user.first_name}'s ɪᴅ: {reply.from_user.id}\nᴄʜᴀᴛ ɪᴅ: {message.chat.id}"
        )
    else:
        message.reply(f"ʏᴏᴜʀ ɪᴅ: {message.from_user.id}\nᴄʜᴀᴛ ɪᴅ: {message.chat.id}")


####


@app.on_message(filters.command("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


__MODULE__ = "🍷 𝐔𖾗𖾝𖾖 𝐈𖽴 😻"
__HELP__ = """
## Usᴇʀ ID Cᴏᴍᴍᴀɴᴅs Hᴇᴘ

### 1. /ᴍᴇ
**Dᴇsᴄʀɪᴘᴛɪᴏɴ:**
Gᴇᴛ ʏᴏᴜʀ ᴀɴᴅ ʀᴇᴘɪᴇᴅ ᴜsᴇʀ's IDs ᴀᴏɴɢ ᴡɪᴛʜ ᴄʜᴀᴛ ID.

**Usᴀɢᴇ:**
/ᴍᴇ [ʀᴇᴘʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]

**Dᴇᴛᴀɪs:**
- Rᴇᴛʀɪᴇᴠᴇs ʏᴏᴜʀ Tᴇᴇɢʀᴀᴍ ID ᴀɴᴅ ᴛʜᴇ ID ᴏғ ᴛʜᴇ ᴜsᴇʀ ʏᴏᴜ ʀᴇᴘɪᴇᴅ ᴛᴏ.
- Asᴏ ᴘʀᴏᴠɪᴅᴇs ᴛʜᴇ ID ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴡʜᴇʀᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ɪs ᴜsᴇᴅ.

### 2. /ɪᴅ [ᴜsᴇʀɴᴀᴍᴇ/ID]
**Dᴇsᴄʀɪᴘᴛɪᴏɴ:**
Gᴇᴛ ᴍᴇssᴀɢᴇ ID, ʏᴏᴜʀ ID, ᴜsᴇʀ's ID (ɪғ ᴘʀᴏᴠɪᴅᴇᴅ), ᴀɴᴅ ᴄʜᴀᴛ ID.

**Usᴀɢᴇ:**
/ɪᴅ [ᴜsᴇʀɴᴀᴍᴇ/ID]

**Dᴇᴛᴀɪs:**
- Rᴇᴛʀɪᴇᴠᴇs ᴛʜᴇ ID ᴏғ ᴛʜᴇ ᴍᴇssᴀɢᴇ, ʏᴏᴜʀ Tᴇᴇɢʀᴀᴍ ID, ᴀɴᴅ ᴛʜᴇ ᴄʜᴀᴛ's ID.
- Iғ ᴀ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ID ɪs ᴘʀᴏᴠɪᴅᴇᴅ, ᴀsᴏ ʀᴇᴛʀɪᴇᴠᴇs ᴛʜᴇ ID ᴏғ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ᴜsᴇʀ.
- Aᴅᴅɪᴛɪᴏɴᴀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ sᴜᴄʜ ᴀs ʀᴇᴘɪᴇᴅ ᴍᴇssᴀɢᴇ ID ᴀɴᴅ ᴄʜᴀᴛ ID ɪs ᴘʀᴏᴠɪᴅᴇᴅ ɪғ ᴀᴘᴘɪᴄᴀʙᴇ.

**Exᴀᴍᴘᴇs:**
- `/ɪᴅ ᴜsᴇʀɴᴀᴍᴇ`
- `/ɪᴅ 123456789`
"""
