import logging
from typing import List

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNELS


async def obunani_tekshir(bot: Bot, user_id: int) -> List[str]:
    """
    Foydalanuvchi obuna BO'LMAGAN kanallar ro'yxatini qaytaradi.
    Bo'sh ro'yxat qaytsa — foydalanuvchi hamma kanalga obuna bo'lgan degani.
    """
    obuna_bolmagan = []

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ("left", "kicked"):
                obuna_bolmagan.append(channel)
        except Exception:
            # Bot kanalda admin bo'lmasa yoki kanal username xato bo'lsa ham,
            # xavfsizlik uchun "obuna bo'lmagan" deb hisoblaymiz
            logging.exception(f"{channel} kanalida obunani tekshirishda xatolik")
            obuna_bolmagan.append(channel)

    return obuna_bolmagan


def obuna_klaviaturasi(obuna_bolmagan_kanallar: List[str]) -> InlineKeyboardMarkup:
    tugmalar = []

    for channel in obuna_bolmagan_kanallar:
        username = channel.lstrip("@")
        tugmalar.append(
            [InlineKeyboardButton(text=f"📢 {channel}", url=f"https://t.me/{username}")]
        )

    tugmalar.append(
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subscription")]
    )

    return InlineKeyboardMarkup(inline_keyboard=tugmalar)


OBUNA_MATNI = (
    "🚫 Botdan foydalanish uchun avval quyidagi kanallarga obuna bo'ling, "
    "so'ngra <b>«✅ Obunani tekshirish»</b> tugmasini bosing:"
)