import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile,Message
from aiogram.filters import Command, CommandStart
import logging  


bot = Bot(token="8899246758:AAF4d2NNyjrM_moTWIqWe28xaO9vAirlzsc")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name},Random media  botimizga xush kelibsiz!")
    await msg.answer("""Bu botda:
🎵 /audio bossangiz random musiqa yuboradi,
📸 /photo bossangiz random rasm yuboradi,
📷 /video bossangiz random video yuboradi
""")
    
    
ADMIN = 7467403246

@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}, botimizga xush kelibsiz!")
    await bot.send_message(chat_id=ADMIN, text=f"Shu odam /start bosdi: \n{msg.from_user.id} - @{msg.from_user.username if msg.from_user.username else "username yo'q"}")

@dp.message(Command("photo"))
async def photo_handler(msg: Message):
    folder = "tgbot/random_media_bot/rasmlar"
    rasmlar = [f"{folder}/{file}" for file in os.listdir(folder)]
    
    file = FSInputFile(random.choice(rasmlar))
    await msg.answer_photo(photo=file, caption = "Mana sizga random rasm!")


@dp.message(Command("vidio"))
async def vidio_handler(msg: Message):
    folder = "tgbot/random_media_bot/vidiolar"
    vidiolar = [f"{folder}/{file}" for file in os.listdir(folder)]
    
    file = FSInputFile(random.choice(vidiolar))
    await msg.answer_vidio(video=file, caption = "Mana sizga random video!")
    
    
@dp.message(Command("audio"))
async def audio_handler(msg: Message):
    folder = "tgbot/random_media_bot/muzikalar"
    muzikalar = [f"{folder}/{file}" for file in os.listdir(folder)]
    
    file = FSInputFile(random.choice(muzikalar))
    await msg.answer_audio(audio=file, caption = "Mana sizga random audio!")
    


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))