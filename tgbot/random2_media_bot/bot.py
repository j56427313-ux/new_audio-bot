import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile,Message
from aiogram.filters import Command, CommandStart
from aiogram.types import Message,ReplyKeyboardMarkup, KeyboardButton
import logging  
ADMIN = 7467403246



bot = Bot(token="8913165582:AAG99wVWTRk21ksLD537hnAoYzvgwk3I_pg")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

buttonlar = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text=" AUDIO qoshish"),KeyboardButton(text="STICKER qoshish")],
    [KeyboardButton(text="PHOTO qoshish")],
    [KeyboardButton(text="VIDEO qoshish")],
    [KeyboardButton(text="GIF qoshish")]
])

@dp.message(CommandStart())
async def salom_ber(msg: Message):
    
    if msg.from_user.id == ADMIN:
        await msg.answer(f"Assalomu aleykum Xo'jayin,nima qoshishni xoxlaysiz!",reply_markup=buttonlar)
    else: 
        await msg.answer(f"Assalomu aleykum {msg.from_user.full_name},Random media  botimizga xush kelibsiz!")
        await msg.answer("""Bu botda:
🎵 /audio bossangiz random musiqa yuboradi,
📸 /photo bossangiz random rasm yuboradi,
📷 /video bossangiz random video yuboradi
""")   
    
@dp.message(F.text == "PHOTO qoshish")
async def photo_btn_admin(msg: Message):
    
    if msg.from_user.id == ADMIN:
        await msg.answer(f"Xo'jayin siz rasm qoshishni bosdingiz\nKerakli rasimni yuboring ")
    else:
        await msg.answer(f"Siz xo'jayin emassiz ❌ ")
    
RASMLAR = []
@dp.message(F.photo == "photo qoshish")
async def photo_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        with open('tgbot/random2_media_bot/rasmlar.txt','a') as file:
             rasm = msg.photo[-1].file_id
             file.write(f"{rasm}\n")
        await msg.answer(f"Rasm qabul qilindi ✅")
    else:
        await msg.answer(f"Siz admin emassiz ❌")
        


@dp.message(Command("photo"))
async def audio_handler(msg: Message):
    with open('tgbot/random2_media_bot/rasmlar.txt','r') as file:
        rasmlar = file.readlines()
        print(rasmlar)
        print("-----------------")
        print(rasmlar[0])
    await msg.answer_photo(photo=random.choice(rasmlar), caption="Tavakkal olinga rasim! ")



@dp.message(F.text == "VIDEO qoshish")
async def video_btn_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer("Xo'jayin siz video qo'shishni bosdingiz\nKerakli videoni yuboring")
    else:
        await msg.answer("Siz xo'jayin emassiz ❌")

@dp.message(F.video)
async def video_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        with open('tgbot/random2_media_bot/videolar.txt', 'a') as file:
            video = msg.video.file_id
            file.write(f"{video}\n")
        await msg.answer("Video qabul qilindi ✅")
    else:
        await msg.answer("Siz admin emassiz ❌")

@dp.message(Command("video"))
async def video_handler(msg: Message):
    with open('tgbot/random2_media_bot/videolar.txt', 'r') as file:
        videolar = [line.strip() for line in file.readlines()]
    await msg.answer_video(video=random.choice(videolar), caption="Tasodifiy video!")


@dp.message(F.text == "AUDIO qoshish")
async def audio_btn_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer("Xo'jayin siz audio qo'shishni bosdingiz\nKerakli audioni yuboring")
    else:
        await msg.answer("Siz xo'jayin emassiz ❌")

@dp.message(F.audio)
async def audio_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        with open('tgbot/random2_media_bot/audiolar.txt', 'a') as file:
            audio = msg.audio.file_id
            file.write(f"{audio}\n")
        await msg.answer("Audio qabul qilindi ✅")
    else:
        await msg.answer("Siz admin emassiz ❌")

@dp.message(Command("audio"))
async def audio_handler(msg: Message):
    with open('tgbot/random2_media_bot/audiolar.txt', 'r') as file:
        audiolar = [line.strip() for line in file.readlines()]
    await msg.answer_audio(audio=random.choice(audiolar), caption="Tasodifiy audio! 🎵")
    


@dp.message(F.text == "GIF qoshish")
async def gif_btn_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer("Xo'jayin siz GIF qo'shishni bosdingiz\nKerakli GIF'ni yuboring")
    else:
        await msg.answer("Siz xo'jayin emassiz ❌")

@dp.message(F.animation)
async def gif_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        with open('tgbot/random2_media_bot/giflar.txt', 'a') as file:
            gif = msg.animation.file_id
            file.write(f"{gif}\n")
        await msg.answer("GIF qabul qilindi ✅")
    else:
        await msg.answer("Siz admin emassiz ❌")

@dp.message(Command("gif"))
async def gif_handler(msg: Message):
    with open('tgbot/random2_media_bot/giflar.txt', 'r') as file:
        giflar = [line.strip() for line in file.readlines()]
    await msg.answer_animation(animation=random.choice(giflar), caption="Tasodifiy GIF! 🎞")


@dp.message(F.text == "STICKER qoshish")
async def sticker_btn_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer("Xo'jayin siz sticker qo'shishni bosdingiz\nKerakli stickerni yuboring")
    else:
        await msg.answer("Siz xo'jayin emassiz ❌")

@dp.message(F.sticker)
async def sticker_admin(msg: Message):
    if msg.from_user.id == ADMIN:
        with open('tgbot/random2_media_bot/stickerlar.txt', 'a') as file:
            sticker = msg.sticker.file_id
            file.write(f"{sticker}\n")
        await msg.answer("Sticker qabul qilindi ✅")
    else:
        await msg.answer("Siz admin emassiz ❌")

@dp.message(Command("sticker"))
async def sticker_handler(msg: Message):
    with open('tgbot/random2_media_bot/stickerlar.txt', 'r') as file:
        stickerlar = [line.strip() for line in file.readlines()]
    await msg.answer_sticker(sticker=random.choice(stickerlar))


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))