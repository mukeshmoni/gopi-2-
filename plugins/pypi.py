import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from VIPMUSIC import app


def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(api_url)
        if response.status_code == 200:
            pypi_info = response.json()
            return pypi_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None


@app.on_message(filters.command("pypi", prefixes="/"))
async def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        pypi_info = get_pypi_info(package_name)

        if pypi_info:
            info_message = (
                f"ᴅᴇᴀʀ {message.from_user.mention} \n "
                f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀᴋᴀɢᴇ ᴅᴇᴛᴀɪʟs \n\n "
                f"ᴘᴀᴋᴀɢᴇ ɴᴀᴍᴇ ➪ {pypi_info['info']['name']}\n\n"
                f"ʟᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ ➪ {pypi_info['info']['version']}\n\n"
                f"ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➪ {pypi_info['info']['summary']}\n\n"
                f"ᴘʀᴏJᴇᴄᴛ ᴜʀʟ ➪ {pypi_info['info']['project_urls']['Homepage']}"
            )
            close_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="〆 ᴄʟᴏsᴇ 〆", callback_data="close")]]
            )
            await message.reply_text(info_message, reply_markup=close_markup)
        else:
            await message.reply_text(
                f"Package '{package_name}' not found \n please dont try again later ."
            )

    except IndexError:
        await message.reply_text(
            "Please provide a package name after the /pypi command."
        )


__MODULE__ = "🍷 𝐏ʏ𖽳𖽹 😻"
__HELP__ = """
**ᴄᴏᴍᴍᴀɴᴅs:**
• /pypi <package_name>`: Get details about a specified Python package from PyPI.

**ɪɴғᴏ:**
ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴀʟʟᴏᴡs ᴜsᴇʀs ᴛᴏ ғᴇᴛᴄʜ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴘʏᴛʜᴏɴ ᴘᴀᴄᴋᴀɢᴇs ғʀᴏᴍ ᴘʏᴘɪ, ɪɴᴄʟᴜᴅɪɴɢ ᴛʜᴇ ᴘᴀᴄᴋᴀɢᴇ ɴᴀᴍᴇ, ʟᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ, ᴅᴇsᴄʀɪᴘᴛɪᴏɴ, ᴀɴᴅ ᴘʀᴏᴊᴇᴄᴛ ᴜʀʟ.

**ɴᴏᴛᴇ:**
ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴘᴀᴄᴋᴀɢᴇ ɴᴀᴍᴇ ᴀғᴛᴇʀ ᴛʜᴇ `/pypi` ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ᴘᴀᴄᴋᴀɢᴇ ᴅᴇᴛᴀɪʟs.
"""
