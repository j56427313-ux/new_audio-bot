import asyncio
from aiogram import Bot, Dispatcher, F,types
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command, CommandStart
import logging  


bot = Bot(token="8590351370:AAGL1tSAS2sUxz4bA-wab3tUUAofQ_odzYk")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}, botimizga xush kelibsiz!")
ADMIN = 7467403246# @myidbot shu tg botdan o'zini idsi qo'yiladi



@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}, botimizga xush kelibsiz!")
    await bot.send_message(chat_id=ADMIN, text=f"Shu odam /start bosdi: \n{msg.from_user.id} - @{msg.from_user.username if msg.from_user.username else "username yo'q"}")
    
@dp.message(F.text)
async def text_handler(msg: Message):
    await msg.answer(f"Text yozildi:\n{msg.text}")

    
@dp.message(F.photo)
async def photo_handler(msg: Message):
    photo = msg.photo[-1]
    file_id = photo.file_id
    await msg.answer_photo(photo=file_id, caption=f"Rasm yuklandi:")
    

@dp.message(F.document)
async def document_handler(msg: Message):
    document = msg.document
    file_id = document.file_id
    file_name = document.file_name
    await msg.answer_document(document=file_id, caption=f"Hujjat yuklandi: {file_name}")
    


@dp.message(F.voice)
async def voice_handler(msg: Message):
    ovoz = msg.voice
    file_id = ovoz.file_id
    await msg.answer_voice(voice=file_id, caption=f"Shu ovozli xabar qabul qilindi!")
    


@dp.message(F.video_note)
async def voice_handler(msg: Message):
    video = msg.video_note
    file_id = video.file_id
    await msg.answer_video_note(video_note=file_id)
    
# ✅ ANIMATION (GIF yuborish)
@dp.message(Command("animation"))
async def send_animation(msg: Message):
    # 1. File ID bilan (eng oson)
    await msg.answer_animation(animation="FILE_ID_bu_yerga")
    
    # 2. URL bilan  
    await msg.answer_animation(animation="https://media.giphy.com/media/abc123/giphy.gif")
    
    # 3. Lokal fayl bilan
    file = FSInputFile("animation.gif")
    await msg.answer_animation(animation=file, caption="Bu GIF 🎬")


# ✅ STICKER yuborish
@dp.message(Command("sticker"))
async def send_sticker(msg: Message):
    # 1. File ID bilan (Telegramdan olingan sticker ID)
    await msg.answer_sticker(sticker="CAACAgIAAxkBAAIB...")  # haqiqiy sticker file_id
    
    # 2. Lokal .webp fayl bilan
    file = FSInputFile("sticker.webp")
    await msg.answer_sticker(sticker=file)


# ✅ VIDEO yuborish
@dp.message(Command("video"))
async def send_video(msg: Message):
    # 1. File ID bilan
    await msg.answer_video(video="FILE_ID_bu_yerga")
    
    # 2. URL bilan
    await msg.answer_video(video="https://example.com/video.mp4")
    
    # 3. Lokal fayl bilan
    file = FSInputFile("video.mp4")
    await msg.answer_video(
        video=file,
        caption="Bu video 🎥",
        width=1280,
        height=720,
        duration=30      # soniyada
    )



@dp.message()
async def get_file_id(msg: Message):
    if msg.animation:
        print("ANIMATION file_id:", msg.animation.file_id)
    elif msg.sticker:
        print("STICKER file_id:", msg.sticker.file_id)
    elif msg.video:
        print("VIDEO file_id:", msg.video.file_id)
# animation, sticker, video



TOKEN = "BOT_TOKENINGIZNI_YOZING"
ADMIN = 123456789   # o'z Telegram ID raqamingizni yozing


bot = Bot(token="8590351370:AAEr9V-6QqLFOWZju74tbG1SYH1B2xAOujc")
dp = Dispatcher()


# START komandasi
@dp.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(
        f"👋 Salom, {msg.from_user.first_name}!\n\n"
        f"⚽ Futbolchi rasmlari botiga xush kelibsiz!\n\n"
        f"🔎 Futbolchi ismini yozing:\n\n"
        f"🇵🇹 Ronaldo\n"
        f"🇦🇷 Messi\n"
        f"🇪🇸 Yamal\n"
        f"🇫🇷 Mbappe\n"
        f"🇧🇪 Hazard\n"
        f"🇳🇴 Holand\n"
        f"🇺🇿 Xusanov\n"
        f"🇧🇷 Vini Jr\n"
        f"🇪🇬 Salah\n"
        f"🇵🇹 Pepe\n\n"
        f"Masalan: Messi"
    )


# Futbolchilar
@dp.message(F.text)
async def text_handler(msg: Message):

    ism = msg.text.lower()

    if ism == 'ronaldo':
        await msg.answer_photo(
            photo="https://tinyurl.com/3cxrnfwx",
            caption="🇵🇹 Cristiano Ronaldo\n🏟 Al Nassr\n📌 Hujumchi\n⭐ 5 marta Oltin to'p sohibi"
        )


    elif ism == 'messi':
        await msg.answer_photo(
            photo="https://tinyurl.com/324ptfwe",
            caption="🇦🇷 Lionel Messi\n🏟 Inter Miami\n📌 Hujumchi\n⭐ 8 marta Oltin to'p sohibi"
        )


    elif ism == 'yamal':
        await msg.answer_photo(
            photo="https://images.serenashirt.com/2024/08/Lamine-Yamal-Barcelona-meme-ornament-Christmas-Ornament.jpg",
            caption="🇪🇸 Lamine Yamal\n🏟 FC Barcelona\n📌 Hujumchi\n⭐ Eng yosh EURO g'olibi"
        )


    elif ism in ('mbappe','mbappé'):
        await msg.answer_photo(
            photo="",
            caption="🇫🇷 Kylian Mbappé\n🏟 Real Madrid\n📌 Hujumchi\n⭐ 2018 Jahon chempioni"
        )


    elif ism == 'hazard':
        await msg.answer_photo(
            photo="https://i.pinimg.com/736x/ff/61/c1/ff61c1e835f1bbe7ed4f1621a2453597.jpg",
            caption="🇧🇪 Eden Hazard\n🏟 Nafaqa\n📌 Yarim himoyachi"
        )


    elif ism in ('holand','holland'):
        await msg.answer_photo(
            photo="https://shorturl.at/g2UyU",
            caption="🇳🇴 Erling Haaland\n🏟 Manchester City\n📌 Hujumchi"
        )


    elif ism == 'xusanov':
        await msg.answer_photo(
            photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS25pdQBBCkxothypNK3AYSGd9hJ48OiKfxFQ&s",
            caption="🇺🇿 Abdukodir Xusanov\n🏟 Manchester City\n📌 Himoyachi"
        )


    elif ism in ('vini','vini jr'):
        await msg.answer_photo(
            photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxblb5jyPflNaTqfA1ktbHIjRICHl_eFI9nQ&s",
            caption="🇧🇷 Vinicius Jr\n🏟 Real Madrid\n📌 Hujumchi"
        )


    elif ism == 'salah':
        await msg.answer_photo(
            photo="https://www.thickaccent.com/wp-content/uploads/2024/10/Vulgar-Mohamed-Salah-Banner-with-Camels-Reappears-Again.jpg",
            caption="🇪🇬 Mohamed Salah\n🏟 Liverpool\n📌 Hujumchi"
        )


    elif ism == 'pepe':
        await msg.answer_photo(
            photo="https://cdn.resfu.com/scripts/tmp_images/goal_pepe_5od3rtf0alhi14pgyil6h5p6u.jpg?size=1200x&lossy=1",
            caption="🇵🇹 Pepe\n🏟 Nafaqa\n📌 Himoyachi"
        )


    else:
        await msg.answer(
            "❌ Bunday futbolchi topilmadi\n\n"
            "✅ Futbolchilar:\n"
            "ronaldo | messi | yamal\n"
            "mbappe | hazard | haaland\n"
            "xusanov | vini | salah | pepe"
        )


    # Admin xabari
    if msg.from_user.id != ADMIN:
        await bot.send_message(
            chat_id=ADMIN,
            text=f"👤 Foydalanuvchi:\n"
                 f"{msg.from_user.id}\n"
                 f"@{msg.from_user.username}\n\n"
                 f"✏️ Yozdi: {msg.text}"
        )


# Rasm qabul qilish
@dp.message(F.photo)
async def photo_handler(msg: Message):
    photo = msg.photo[-1]
    await msg.answer_photo(
        photo=photo.file_id,
        caption="✅ Rasm qabul qilindi"
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

async def main():
    await dp.start_polling(bot)
    



asyncio.run(main())
   
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))