import datetime
from re import findall

from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from VIPMUSIC import app
from VIPMUSIC.misc import SUDOERS
from .notes import extract_urls
from VIPMUSIC.utils.database import is_gbanned_user
from utils import (
    del_goodbye,
    get_goodbye,
    set_goodbye,
    is_greetings_on,
    set_greetings_on,
    set_greetings_off,
)
from utils.error import capture_err
from VIPMUSIC.utils.functions import check_format, extract_text_and_keyb
from VIPMUSIC.utils.keyboard import ikb
from utils.permissions import adminsOnly


async def handle_left_member(member, chat):

    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} ᴡᴀs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ, ᴀɴᴅ ɢᴏᴛ ʀᴇᴍᴏᴠᴇᴅ,"
                + " ɪғ ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜɪs ɪs ᴀ ғᴀʟsᴇ ɢʙᴀɴ, ʏᴏᴜ ᴄᴀɴ ᴀᴘᴘᴇᴀʟ"
                + " ғᴏʀ ᴛʜɪs ʙᴀɴ ɪɴ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ",
            )
            return
        if member.is_bot:
            return
        return await send_left_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_message(filters.left_chat_member & filters.group, group=6)
@capture_err
async def goodbye(_, m: Message):
    if m.from_user:
        member = await app.get_users(m.from_user.id)
        chat = m.chat
        return await handle_left_member(member, chat)


async def send_left_message(chat: Chat, user_id: int, delete: bool = False):
    is_on = await is_greetings_on(chat.id, "goodbye")

    if not is_on:
        return

    goodbye, raw_text, file_id = await get_goodbye(chat.id)

    if not raw_text:
        return

    text = raw_text
    keyb = None

    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    u = await app.get_users(user_id)

    replacements = {
        "{NAME}": u.mention,
        "{ID}": f"`{user_id}`",
        "{FIRSTNAME}": u.first_name,
        "{GROUPNAME}": chat.title,
        "{SURNAME}": u.last_name or "None",
        "{USERNAME}": u.username or "None",
        "{DATE}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{WEEKDAY}": datetime.datetime.now().strftime("%A"),
        "{TIME}": datetime.datetime.now().strftime("%H:%M:%S") + " UTC",
    }

    for placeholder, value in replacements.items():
        if placeholder in text:
            text = text.replace(placeholder, value)

    if goodbye == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif goodbye == "Photo":
        m = await app.send_photo(
            chat.id,
            photo=file_id,
            caption=text,
            reply_markup=keyb,
        )
    else:
        m = await app.send_animation(
            chat.id,
            animation=file_id,
            caption=text,
            reply_markup=keyb,
        )


@app.on_message(filters.command("setgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def set_goodbye_func(_, message):
    usage = "Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ, ɢɪғ ᴏʀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ.\n\nᴏᴛᴇs: ᴄᴀᴘᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ ғᴏʀ ɢɪғ ᴀɴᴅ ᴘʜᴏᴛᴏ."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="More Help",
                    url=f"t.me/{app.username}?start=greetings",
                )
            ],
        ]
    )
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    try:
        if not replied_message:
            await message.reply_text(usage, reply_markup=key)
            return
        if replied_message.animation:
            goodbye = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            goodbye = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            goodbye = "Text"
            file_id = None
            text = replied_message.text
            raw_text = text.markdown
        if replied_message.reply_markup and not findall(r"\[.+\,.+\]", raw_text):
            urls = extract_urls(replied_message.reply_markup)
            if urls:
                response = "\n".join(
                    [f"{name}=[{text}, {url}]" for name, text, url in urls]
                )
                raw_text = raw_text + response
        raw_text = await check_format(ikb, raw_text)
        if raw_text:
            await set_goodbye(chat_id, goodbye, raw_text, file_id)
            return await message.reply_text(
                "ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ."
            )
        else:
            return await message.reply_text(
                "Wʀᴏɴɢ ғᴏʀᴍᴀᴛᴛɪɴɢ, ᴄʜᴇᴄᴋ ᴛʜᴇ ʜᴇʟᴘ sᴇᴄᴛɪᴏɴ.\n\n**Usᴀsɢᴇ:**\nTᴛᴇxᴛ: `Text`\nᴛᴇxᴛ + ʙᴜᴛᴛᴏɴs: `Text ~ Buttons`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**Oɴʟʏ Tᴇxᴛ, Gɪғ ᴀɴᴅ Pʜᴏᴛᴏ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.**"
        )


@app.on_message(filters.command(["delgoodbye", "deletegoodbye"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_goodbye_func(_, message):
    chat_id = message.chat.id
    await del_goodbye(chat_id)
    await message.reply_text("Gᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ")


@app.on_message(filters.command("goodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def goodbye(client, message: Message):
    command = message.text.split()

    if len(command) == 1:
        return await get_goodbye_func(client, message)

    if len(command) == 2:
        action = command[1].lower()
        if action in ["on", "enable", "y", "yes", "true", "t"]:
            success = await set_greetings_on(message.chat.id, "goodbye")
            if success:
                await message.reply_text(
                    "I'ʟʟ ʙᴇ sᴀʏɪɴɢ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴀɴʏ ʟᴇᴀᴠᴇʀs ғʀᴏᴍ ɴᴏᴡ ᴏɴ!"
                )
            else:
                await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴇɴᴀʙʟᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs.")

        elif action in ["off", "disable", "n", "no", "false", "f"]:
            success = await set_greetings_off(message.chat.id, "goodbye")
            if success:
                await message.reply_text("I'ʟʟ sᴛᴀʏ ǫᴜɪᴇᴛ ᴡʜᴇɴ ᴘᴇᴏᴘʟᴇ ʟᴇᴀᴠᴇ.")
            else:
                await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅɪsᴀʙʟᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs.")

        else:
            await message.reply_text(
                "Iɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ. Pʟᴇᴀsᴇ ᴜsᴇ:\n"
                "/goodbye - Tᴏ ɢᴇᴛ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ\n"
                "/goodbye [on, y, true, enable, t] - ᴛᴏ ᴛᴜʀɴ ᴏɴ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
                "/goodbye [off, n, false, disable, f, no] - ᴛᴏ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
                "/delgoodbye ᴏʀ /deletegoodbye ᴛᴏ ᴅᴇʟᴛᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ"
            )
    else:
        await message.reply_text(
            "Iɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ. Pʟᴇᴀsᴇ ᴜsᴇ:\n"
            "/goodbye - Tᴏ ɢᴇᴛ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ\n"
            "/goodbye [on, y, true, enable, t] - ᴛᴏ ᴛᴜʀɴ ᴏɴ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
            "/goodbye [off, n, false, disable, f, no] - ᴛᴏ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
            "/delgoodbye ᴏʀ /deletegoodbye ᴛᴏ ᴅᴇʟᴛᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ"
        )


async def get_goodbye_func(_, message):
    chat = message.chat
    goodbye, raw_text, file_id = await get_goodbye(chat.id)
    if not raw_text:
        return await message.reply_text(
            "Dɪᴅ Yᴏᴜ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴛ's ᴀɴᴛ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ"
        )
    if not message.from_user:
        return await message.reply_text("Yᴏᴜ'ʀᴇ ᴀɴᴏɴ, ᴄᴀɴ'ᴛ sᴇɴᴅ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ.")

    await send_left_message(chat, message.from_user.id)
    is_grt = await is_greetings_on(chat.id, "goodbye")
    text = None
    if is_grt:
        text = "Tʀᴜᴇ"
    else:
        text = "Fᴀʟsᴇ"
    await message.reply_text(
        f'I ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ sᴀʏɪɴɢ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴜsᴇʀs :- {text}\nGᴏᴏᴅʙʏᴇ: {goodbye}\n\nғɪʟᴇ_ɪᴅ: `{file_id}`\n\n`{raw_text.replace("`", "")}`'
    )


__MODULE__ = "🍷 𝐆𖽙𖽙𖽴𖽜𖽙ʏ 😻"
__HELP__ = """
ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ɢᴏᴏᴅʙʏᴇ:

/setgoodbye - Rᴇᴘʟʏ ᴛʜɪs ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴄᴏʀʀᴇᴄᴛ
ғᴏʀᴍᴀᴛ ғᴏʀ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ, ᴄʜᴇᴄᴋ ᴇɴᴅ ᴏғ ᴛʜɪs ᴍᴇssᴀɢᴇ.

/goodbye - Tᴏ ɢᴇᴛ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ

/goodbye  [ᴏɴ, ʏ, ᴛʀᴜᴇ, ᴇɴᴀʙʟᴇ, ᴛ] - ᴛᴏ ᴛᴜʀɴ ᴏɴ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs

/goodbye [ᴏғғ, ɴ, ғᴀʟsᴇ, ᴅɪsᴀʙʟᴇ, ғ, ɴᴏ] - ᴛᴏ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs

/delgoodbye ᴏʀ /deletegoodbye ᴛᴏ ᴅᴇʟᴛᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ
**SetoodBye ->


Tᴏ sᴇᴛ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ɢɪғ ᴀs ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ. Aᴅᴅ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀs ᴄᴀᴘᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴘʜᴏᴛᴏ ᴏʀ ɢɪғ. Tʜᴇ ᴄᴀᴘᴛɪᴏɴ ᴍᴜsᴇ ʙᴇ ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.**

Fᴏʀ ᴛᴇxᴛ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ Jᴜsᴛ sᴇɴᴅ ᴛʜᴇ ᴛᴇxᴛ. Tʜᴇɴ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ

Tʜᴇ ғᴏʀᴍᴀᴛ sʜᴏᴜʟᴅ ʙᴇ sᴏᴍᴇᴛʜɪɴɢ ʟɪᴋᴇ ʙᴇʟᴏᴡ.

Hɪ {NAME} [{ID}] Wᴇʟᴄᴏᴍᴇ ᴛᴏ {GROUPNAME}

~ #Tʜɪs sᴇᴘᴀʀᴀᴛᴇʀ (~) sʜᴏᴜʟᴅ ʙᴇ ᴛʜᴇʀᴇ ʙᴇᴛᴡᴇᴇɴ ᴛᴇxᴛ ᴀɴᴅ ʙᴜᴛᴛᴏɴs, ʀᴇᴍᴏᴠᴇ ᴛʜɪs ᴄᴏᴍᴍᴇɴᴛ ᴀʟsᴏ

Button=[Dᴜᴄᴋ, ʜᴛᴛᴘs://ᴅᴜᴄᴋᴅᴜᴄᴋɢᴏ.ᴄᴏᴍ]
Button2=[Gɪᴛʜᴜʙ, ʜᴛᴛᴘs://ɢɪᴛʜᴜʙ.ᴄᴏᴍ]
**NOTES ->**

Cʜᴇᴄᴋᴏᴜᴛ /markdownhelp ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ғᴏʀᴍᴀᴛᴛɪɴɢs ᴀɴᴅ ᴏᴛʜᴇʀ sʏɴᴛᴀx.
"""
