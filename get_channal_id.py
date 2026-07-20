"""
PRIVATE KANAL ID SINI TOPISH UCHUN VAQTINCHA SKRIPT
=====================================================
1. Botni (@wikipeia_bot) o'z private kanalingizga ADMIN qilib qo'shing.
2. Shu skriptni ishga tushiring:  python get_channel_id.py
3. Kanalga istalgan xabar yozing (yoki eski xabarni forward qiling).
4. Konsolda "KANAL ID:" deb chiqqan raqamni (masalan -1001234567890) nusxalab oling.
5. Skriptni to'xtating (Ctrl+C) va o'sha raqamni config.py dagi CHANNEL_ID ga qo'ying.
6. Bu skriptni endi ishlatish shart emas, uni o'chirib tashlashingiz mumkin.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.channel_post()
async def har_qanday_kanal_xabari(msg: Message):
    print("\n" + "=" * 50)
    print(f"KANAL ID: {msg.chat.id}")
    print(f"KANAL NOMI: {msg.chat.title}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))