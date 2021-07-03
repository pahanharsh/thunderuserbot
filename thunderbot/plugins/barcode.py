"""BarCode Generator with text
Command .barcode (your text)
"""

import asyncio
import os
from datetime import datetime

import barcode
from barcode.writer import ImageWriter
from thunderbot.utils import admin_cmd

from thunderbot import CMD_HELP


@thunderbot.on(admin_cmd(pattern="barcode ?(.*)"))
@thunderbot.on(sudo_cmd(pattern="barcode ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await eor(event, "...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await borg.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        await eor(event, str(e))
        return
    end = datetime.now()
    ms = (end - start).seconds
    await eor(event, "Created BarCode in {} seconds".format(ms))
    await asyncio.sleep(5)
    await event.delete()


CMD_HELP.update(
    {"barcode": ".barcode <text>\nUse - For making barcode that contains text."}
)
