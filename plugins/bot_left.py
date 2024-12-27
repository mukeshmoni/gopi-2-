import random

from pyrogram import filters
from pyrogram.types import Message

from config import LOG_GROUP_ID
from VIPMUSIC import app
from VIPMUSIC.utils.database import delete_served_chat, get_assistant
from VIPMUSIC.utils.database import (
    delete_filter,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
    set_loop,
)
from VIPMUSIC.core.call import VIP

photo = [
    "https://telegra.ph/file/ee9a616090d78437e823f.jpg",
    "https://telegra.ph/file/ee9a616090d78437e823f.jpg",
    "https://telegra.ph/file/ee9a616090d78437e823f.jpg",
    "https://telegra.ph/file/ee9a616090d78437e823f.jpg",
    "https://telegra.ph/file/ee9a616090d78437e823f.jpg",
]


@app.on_message(filters.left_chat_member, group=-12)
async def on_left_chat_member(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == (await app.get_me()).id:
            remove_by = (
                message.from_user.mention if message.from_user else "🍷 𝐔𖽪𝙺𖽡𖽙𖽮 𝐔𖾗𖽞𖽷 😻"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "🍷 𝐏𖽷𖽹ᵥ𖽖𖾓𖽞  𝐂𖽻𖽖𖾓 😻"
            )
            chat_id = message.chat.id
            left = f"✫ <b><u>🍷 𝐋𖽞ꜰ𖾓 𝐆𖽷𖽙𖽪𖽳 😻</u></b> ✫\n\n🍷 𝐂𖽻𖽖𖾓 𝐓𖽹𖾓𖾘𖾔 😻  {title}\n\n🍷 𝐂𖽻𖽖𖾓  𝐈𖽴 😻  {chat_id}\n\n🍷 𝐑𖽞𖽧𖽙ᵥ𖾝 𝐁ʏ 😻 {remove_by}\n\n🍷 𝐁𖽙𖾓  😻 @{app.username}"
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)
            await delete_served_chat(chat_id)
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        return
