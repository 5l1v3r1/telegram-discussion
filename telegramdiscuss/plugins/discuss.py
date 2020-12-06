import time
from functools import partial
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegramdiscuss.BotConfig import QA_Bot
from pyrogram.errors import MessageDeleteForbidden, MessageIdInvalid
import logging
import configparser

config = configparser.ConfigParser()
config.read(f"telegramdiscuss/settings.ini")
DC_GRP = config["discussion"]["DISCUSS_GROUP"]
DC_CHNL = config["discussion"]["DISCUSS_CHANNEL"]
QA_GRP = config["discussion"]["QA_GROUP"]
MSG_CMD = config["discussion"]["MSG_COMMAND"]

command = partial(filters.command, prefixes=["!", "/", "."])
# logging.basicConfig(
#     filename="info.log", format="%(asctime)s - %(message)s", level=logging.INFO
# )


@QA_Bot.on_message(filters.channel)
async def channel_forward(client: Client, message: Message) -> None:
    try:
        await client.forward_messages(
            chat_id=DC_GRP,
            from_chat_id=DC_CHNL,
            message_ids=[message.message_id],
        )
    except MessageIdInvalid:
        return None  # Editing channel info causes MessageIdInvalid


async def msg_delete(client: Client, message: Message) -> None:

    try:
        await message.delete(True)
    except MessageDeleteForbidden:
        await client.send_message(
            chat_id=message.chat.id,
            text="Komut mesajlarını silebilmem için bana yetki vermelisin",
        )


@QA_Bot.on_message(command(MSG_CMD))
async def qa_command(client: Client, message: Message) -> None:

    await msg_delete(client, message)

    if not message.reply_to_message:
        await message.reply_text(
            text="Tartışma kanalına iletmek istediğin mesajı alıntılamalısın."
        )
        return None

    user = message.reply_to_message.from_user
    user_mention = f"[{user.first_name}](tg://user?id={user.first_name})"

    question = message.reply_to_message.text
    qa_message = f"**{user_mention} Sordu:**\n\n{question}"

    qa_chn_msg = await client.send_message(
        chat_id=DC_CHNL, text=qa_message, disable_notification=True
    )

    # https://t.me/c/<channel_id>/<message_id>
    # https://t.me/<channel_name>/<message_id>
    tg_url = "https://t.me/"
    channel_url = (
        f"{tg_url}c/{DC_CHNL[4:]}" if DC_CHNL[4:].isdigit() else f"{tg_url}{DC_CHNL}"
    )

    qa_button = InlineKeyboardButton(
        text="Soruya Git",
        url=f"{channel_url}/{qa_chn_msg.message_id}",
    )

    await client.send_message(
        chat_id=QA_GRP,
        text=f"**{user_mention} Sordu:**\n\n{question}\n\nSoru başlığına gitmek için tıkla",
        reply_markup=InlineKeyboardMarkup([[qa_button]]),
    )


@QA_Bot.on_message(command("activate"))
async def activate(client: Client, message: Message) -> None:

    activation = await client.send_message(
        chat_id=message.chat.id, text="Botu kullanmaya başlayabilirsin"
    )
    time.sleep(2)
    await client.delete_messages(
        chat_id=message.chat.id, message_ids=[activation.message_id]
    )
