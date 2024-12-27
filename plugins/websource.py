import requests
from pyrogram import filters
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from VIPMUSIC import app


def download_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return (
                f"Failed to download source code. Status code: {response.status_code}"
            )

    except Exception as e:
        return f"An error occurred: {str(e)}"


# Handler for /webdl command to download website source code
@app.on_message(filters.command("webdl"))
def web_download(client, message):
    # Check if the command has a URL attached
    if len(message.command) == 1:
        message.reply_text("Please enter a URL along with the /webdl command.")
        return

    # Get the URL after /webdl command
    url = message.command[1]

    source_code = download_website(url)
    if source_code.startswith("An error occurred") or source_code.startswith(
        "Failed to download"
    ):
        message.reply_text(source_code)
    else:
        # Save the source code to a file
        with open("website.txt", "w", encoding="utf-8") as file:
            file.write(source_code)
        message.reply_document(document="website.txt", caption=f"Source code of {url}")


__MODULE__ = "🍷 𝐖𖽞𖽴𖽙𖾘 😻"
__HELP__ = """
**ᴄᴏᴍᴍᴀɴᴅ:**

• /webdl - **ᴅᴏᴡɴʟᴏᴀᴅ ᴡᴇʙsɪᴛᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ.**

**ɪɴғᴏ:**

- ᴛʜɪs ʙᴏᴛ ᴘʀᴏᴠɪᴅᴇs ᴀ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ᴏғ ᴀ ᴡᴇʙsɪᴛᴇ.
- ᴜsᴇ /webdl ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜ ᴀ ᴜʀʟ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ᴏғ ᴛʜᴇ ᴡᴇʙsɪᴛᴇ.

**ɴᴏᴛᴇ:**

- ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴡᴇʙsɪᴛᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ.
- ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ᴡɪʟʟ ʙᴇ sᴀᴠᴇᴅ ᴀs ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ ᴀɴᴅ sᴇɴᴛ ᴀs ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ.
"""
