from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls.types.input_stream import InputAudioStream
from Client import callsmusic, queues

import converter
from youtube import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, AUD_IMG, QUE_IMG
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(command(["audio", f"audio@J_a_n_a_M_U_S_I_C_bot"]) & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("๐ **ูุนุงูุฌุฉ** ุงูููุณููู...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="แฏหน ๐๐ผ๐๐ฝ๐๐๐ฃฅโโโโโ๐ต๐ธูููุจูููุฑูอข",
                        url=f"https://t.me/D_A_D_S_A_K_R_A_N_N"),
                    InlineKeyboardButton(
                        text="๐๐๐๐๐๐๐",
                        url=f"https://t.me/SOURCESAKRAN")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"ูุฏุฉ ุงูููุทุน ุงุทูู ูู {DURATION_LIMIT} ุบูุฑ ูุณููุญ ูู ุจุชุดุบูููุง"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("ูู ุงุฌุฏ ุงูููุณููู ูุชุดุบูููุง !")
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=QUE_IMG,
        reply_markup=keyboard,
        caption=f"#โฃ ุทูุจู ูู ูุงุฆูุฉ ุงูุงูุชุธุงุฑ ุงูุฏูุฑ {position}")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(
                message.chat.id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            ) 
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=AUD_IMG,
        reply_markup=keyboard,
        caption=f"๐ง ุงุดุชุบูุช ุงูุงุบููุฉ ุงููุทููุจุฉ ุจูุณุทุฉ {costumer}"
        )
        return await lel.delete()
