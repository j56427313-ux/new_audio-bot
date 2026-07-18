import asyncio
import os
import re
import shutil
from typing import Any, Awaitable, Callable, Dict
from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.types import Message, FSInputFile, TelegramObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command, CommandStart
import logging  
import wikipedia  # pip install wikipedia
from buttons import menyu, ovoz_menyu, rasm_menyu, orqaga_menyu, RASM_FILTRLARI
from config import API_TOKEN, CHANNEL_USERNAME, CHANNEL_URL, Admin
from aiogram.fsm.state import State
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
import instaloader

from audio_utils import matnni_ovozga_aylantir, ovozni_matnga_aylantir
from image_utils import (
    oq_qora_qilish,
    blur_qilish,
    cartoon_effekt,
    fon_ochirish,
    yuz_mesh_filtri,
    matnni_ochirish,
)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


# ====================== MAJBURIY OBUNA ======================

async def obunani_tekshirish(user_id: int) -> bool:
    """Foydalanuvchi kanalga obuna bo'lganmi-yo'qmi tekshiradi.
    Bot kanalda ADMIN bo'lishi shart, aks holda bu tekshiruv ishlamaydi."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        )
    except Exception as e:
        logging.warning(f"Obunani tekshirishda xatolik: {e}")
        return False


def obuna_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")],
        ]
    )


OBUNA_XABARI = (
    "❗️ Botdan foydalanish uchun avval quyidagi kanalga obuna bo'ling,\n"
    "so'ngra \"✅ Obunani tekshirish\" tugmasini bosing:"
)


class ObunaMiddleware(BaseMiddleware):
    """/start buyrug'idan tashqari barcha xabarlarni obuna bo'lmagan
    foydalanuvchilar uchun bloklaydi."""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)

        if not await obunani_tekshirish(event.from_user.id):
            await event.answer(OBUNA_XABARI, reply_markup=obuna_keyboard())
            return

        return await handler(event, data)


class AdminGaKorsatishMiddleware(BaseMiddleware):
    """Foydalanuvchilar yozgan barcha xabarlarni (matn, rasm, ovoz va h.k.)
    ADMIN'ga forward qilib turadi, shunda admin foydalanuvchilar bilan
    botning "suhbatini" kuzatib borishi mumkin. Admin'ning o'zi yozgan
    xabarlar (masalan sinov uchun) qayta o'ziga forward qilinmaydi."""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user and event.from_user.id != Admin:
            try:
                foydalanuvchi = event.from_user
                sarlavha = (
                    f"👤 {foydalanuvchi.full_name} "
                    f"(@{foydalanuvchi.username or 'username_yoq'}, id: {foydalanuvchi.id})"
                )
                await bot.send_message(chat_id=Admin, text=sarlavha)
                await bot.forward_message(
                    chat_id=Admin,
                    from_chat_id=event.chat.id,
                    message_id=event.message_id,
                )
            except Exception as e:
                logging.warning(f"Adminga xabarni forward qilishda xatolik: {e}")

        return await handler(event, data)


dp.message.middleware(AdminGaKorsatishMiddleware())
dp.message.middleware(ObunaMiddleware())


@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(call: CallbackQuery):
    if await obunani_tekshirish(call.from_user.id):
        await call.message.delete()
        await call.message.answer(
            f"✅ Obuna tasdiqlandi! Assalomu aleykum {call.from_user.full_name}, "
            f"WIKIPEDIA botimizga xush kelibsiz!",
            reply_markup=menyu,
        )
        await call.answer()
    else:
        await call.answer("❌ Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    if await obunani_tekshirish(msg.from_user.id):
        await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}, WIKIPEDIA botimizga xush kelibsiz!", reply_markup=menyu)
    else:
        await msg.answer(OBUNA_XABARI, reply_markup=obuna_keyboard())
    

@dp.message(F.text == "Wikipedia 📝")
async def wiki_handler(msg: Message, state: FSMContext):
    await msg.reply("Wikipedia bo'limiga kirdingiz, savol bering:", reply_markup=orqaga_menyu)
    await state.set_state("wiki_savol")


@dp.message(StateFilter("wiki_savol"), F.text == "⬅️ Orqaga")
async def wiki_orqaga_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Bosh menyu:", reply_markup=menyu)


@dp.message(StateFilter("wiki_savol"))
async def wiki_savol_handler(msg: Message, state: FSMContext):
    savol = msg.text 
    # find first result from wikipedia
    try:
        javob = wikipedia.summary(savol)
        await msg.answer(javob, reply_markup=menyu)
    except Exception as e:
        await msg.answer("Kechirasiz, bu mavzu bo'yicha ma'lumot topilmadi.", reply_markup=menyu)
    await state.clear()


@dp.message(F.text == "Harry Potter 📚")
async def harry_potter_handler(msg: Message, state: FSMContext):
    await msg.answer("Harry Potter bo'limiga kirdingiz, qaysi qahramon haqida ma'lumot olishni xohlaysiz? (Masalan: Harry Potter, Hermione Granger, Ron Weasley)", reply_markup=ReplyKeyboardRemove())
    await state.set_state("harry_potter_qahramon")
    
    
import requests # pip install requests
@dp.message(StateFilter("harry_potter_qahramon"))
async def harry_potter_qahramon_handler(msg: Message, state: FSMContext):
    qahramon = msg.text.lower()
    try:
        data = requests.get("https://hp-api.onrender.com/api/characters").json()
    except Exception:
        await msg.answer("❌ Ma'lumot olishda xatolik yuz berdi, birozdan so'ng qayta urinib ko'ring.", reply_markup=menyu)
        await state.clear()
        return

    topilgan_hero = None
    for hero in data:
        if qahramon in hero['name'].lower():
            topilgan_hero = hero
            break

    if topilgan_hero is None:
        await msg.answer("Kechirasiz, bu qahramon topilmadi.", reply_markup=menyu)
        await state.clear()
        return

    ism = topilgan_hero['name']
    uy = topilgan_hero['house'] or "Noma'lum"
    rasm = topilgan_hero['image'] if topilgan_hero['image'] else None
    hayotda = topilgan_hero['actor'] or "Noma'lum"
    yili = topilgan_hero['yearOfBirth'] or "Noma'lum"

    caption = f"👤 Ism: {ism}\n🏠 Uy: {uy}\n👨‍💼 Hayotdagi ismi: {hayotda}\n🎂Tug'ilgan yili: {yili}"
    if rasm is not None:
        await msg.answer_photo(photo=rasm, caption=caption, reply_markup=menyu)
    else:
        await msg.answer(caption, reply_markup=menyu)
    await state.clear()
    
    


# Ko'rsatiladigan valyutalar kodi va bayrog'i
CURRENCIES = [
    ("USD", "🇺🇸"),
    ("EUR", "🇪🇺"),
    ("RUB", "🇷🇺"),
    ("GBP", "🇬🇧"),
    ("JPY", "🇯🇵"),
    ("KZT", "🇰🇿"),
]


@dp.message(F.text == "Valyuta 💰")
async def valyuta_handler(msg: Message):
    try:
        data = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
    except Exception:
        await msg.answer("❌ Valyuta kurslarini olishda xatolik yuz berdi, birozdan so'ng qayta urinib ko'ring.", reply_markup=menyu)
        return

    javob = "💱 <b>Bugungi valyuta kurslari (O'zbekiston Markaziy banki)</b>\n\n"
    sana = None
    topildi_soni = 0

    for code, bayroq in CURRENCIES:
        valyuta = next((c for c in data if c.get("Ccy") == code), None)
        if valyuta:
            nominal = valyuta.get("Nominal", "1")
            kurs = valyuta.get("Rate")
            javob += f"{bayroq} {nominal} {code} => {kurs} so'm\n"
            sana = valyuta.get("Date")
            topildi_soni += 1

    if topildi_soni == 0:
        await msg.answer("Valyuta ma'lumotlari topilmadi.", reply_markup=menyu)
        return

    if sana:
        javob += f"\n📅 Sana: {sana}"

    await msg.answer(javob, reply_markup=menyu, parse_mode="HTML")


# ====================== INSTAGRAM YUKLAB OLISH ======================
INSTA_DOWNLOAD_DIR = "insta_downloads"
_instaloader_client = instaloader.Instaloader(
    dirname_pattern=INSTA_DOWNLOAD_DIR + "/{shortcode}",
    save_metadata=False,
    download_video_thumbnails=False,
    post_metadata_txt_pattern="",
    quiet=True,
)


def _extract_shortcode(url: str) -> str | None:
    """Instagram post/reel linkidan shortcode'ni ajratib oladi."""
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None


def _download_instagram_post(shortcode: str) -> list[str]:
    """
    Sinxron (bloklovchi) funksiya — instaloader kutubxonasi async emas,
    shuning uchun bu asyncio.to_thread() orqali alohida oqimda chaqiriladi.
    Yuklab olingan fayllar (video/rasm) yo'llari ro'yxatini qaytaradi.
    """
    post = instaloader.Post.from_shortcode(_instaloader_client.context, shortcode)
    _instaloader_client.download_post(post, target=shortcode)

    folder = os.path.join(INSTA_DOWNLOAD_DIR, shortcode)
    fayllar = []
    if os.path.isdir(folder):
        for fname in sorted(os.listdir(folder)):
            if fname.lower().endswith((".mp4", ".jpg", ".jpeg", ".png")):
                fayllar.append(os.path.join(folder, fname))
    return fayllar


@dp.message(F.text == "Instagram 📷")
async def instagram_handler(msg: Message, state: FSMContext):
    await msg.answer(
        "📷 Instagram bo'limiga kirdingiz.\n\n"
        "Post yoki Reels linkini yuboring, masalan:\n"
        "https://www.instagram.com/p/XXXXXXXXXXX/",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state("insta_link")


@dp.message(StateFilter("insta_link"))
async def instagram_link_handler(msg: Message, state: FSMContext):
    url = msg.text.strip()
    shortcode = _extract_shortcode(url)

    if not shortcode:
        await msg.answer(
            "❌ Bu Instagram linki noto'g'ri ko'rinishda. Iltimos, to'g'ri link yuboring:\n"
            "https://www.instagram.com/p/XXXXXXXXXXX/",
            reply_markup=menyu,
        )
        await state.clear()
        return

    kutish_xabari = await msg.answer("⏳ Yuklab olinmoqda, biroz kuting...")

    try:
        fayllar = await asyncio.to_thread(_download_instagram_post, shortcode)
    except Exception as e:
        logging.warning(f"Instagram yuklashda xatolik: {e}")
        await kutish_xabari.edit_text(
            "❌ Yuklab olishda xatolik yuz berdi. Post yopiq (private) bo'lishi, "
            "yoki Instagram vaqtincha so'rovlarni cheklayotgan bo'lishi mumkin."
        )
        await msg.answer("Bosh menyu:", reply_markup=menyu)
        await state.clear()
        return

    await kutish_xabari.delete()

    if not fayllar:
        await msg.answer("❌ Bu link bo'yicha video yoki rasm topilmadi.", reply_markup=menyu)
        await state.clear()
        return

    for fayl_path in fayllar:
        try:
            if fayl_path.lower().endswith(".mp4"):
                await msg.answer_video(video=FSInputFile(fayl_path))
            else:
                await msg.answer_photo(photo=FSInputFile(fayl_path))
        except Exception as e:
            logging.warning(f"Faylni yuborishda xatolik ({fayl_path}): {e}")

    await msg.answer("✅ Yuklab olindi!", reply_markup=menyu)

    # Vaqtincha fayllarni tozalash
    shutil.rmtree(os.path.join(INSTA_DOWNLOAD_DIR, shortcode), ignore_errors=True)
    await state.clear()




# ====================== 🎙️ OVOZ BO'LIMI (TTS / STT) ======================

@dp.message(F.text == "Ovoz 🎙️")
async def ovoz_bolim_handler(msg: Message, state: FSMContext):
    await msg.answer("🎙️ Ovoz bo'limi. Kerakli funksiyani tanlang:", reply_markup=ovoz_menyu)
    await state.set_state("ovoz_bolim")


@dp.message(StateFilter("ovoz_bolim"), F.text == "⬅️ Orqaga")
async def ovoz_orqaga_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Bosh menyu:", reply_markup=menyu)


@dp.message(StateFilter("ovoz_bolim"), F.text == "🗣 Matn → Ovoz")
async def tts_boshlash_handler(msg: Message, state: FSMContext):
    await msg.answer("✍️ Ovozga aylantirish uchun matn yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("tts_matn_kutish")


@dp.message(StateFilter("tts_matn_kutish"))
async def tts_generate_handler(msg: Message, state: FSMContext):
    matn = msg.text
    if not matn:
        await msg.answer("❗️ Iltimos, matn ko'rinishida yuboring.")
        return

    kutish = await msg.answer("⏳ Ovoz yaratilmoqda...")
    fayl_path = f"tts_{msg.from_user.id}.mp3"
    try:
        await matnni_ovozga_aylantir(matn, fayl_path)
        await msg.answer_voice(voice=FSInputFile(fayl_path))
    except Exception as e:
        logging.warning(f"TTS xatolik: {e}")
        await msg.answer("❌ Ovoz yaratishda xatolik yuz berdi.")
    finally:
        if os.path.exists(fayl_path):
            os.remove(fayl_path)
        await kutish.delete()

    await msg.answer("Yana davom etamizmi?", reply_markup=ovoz_menyu)
    await state.set_state("ovoz_bolim")


@dp.message(StateFilter("ovoz_bolim"), F.text == "🎧 Ovoz → Matn")
async def stt_boshlash_handler(msg: Message, state: FSMContext):
    await msg.answer("🎤 Ovozli xabar yoki audio fayl yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("stt_audio_kutish")


@dp.message(StateFilter("stt_audio_kutish"), F.voice | F.audio)
async def stt_process_handler(msg: Message, state: FSMContext):
    kutish = await msg.answer("⏳ Matnga aylantirilmoqda...")

    file_id = msg.voice.file_id if msg.voice else msg.audio.file_id
    fayl = await bot.get_file(file_id)
    local_path = f"stt_{msg.from_user.id}.ogg"
    await bot.download_file(fayl.file_path, local_path)

    try:
        matn = await ovozni_matnga_aylantir(local_path)
        if matn:
            await kutish.edit_text(f"📝 Natija:\n\n{matn}")
        else:
            await kutish.edit_text("❌ Ovozdan matn aniqlanmadi.")
    except Exception as e:
        logging.warning(f"STT xatolik: {e}")
        await kutish.edit_text("❌ Ovozni matnga aylantirishda xatolik yuz berdi.")
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

    await msg.answer("Yana davom etamizmi?", reply_markup=ovoz_menyu)
    await state.set_state("ovoz_bolim")


@dp.message(StateFilter("stt_audio_kutish"))
async def stt_notoggri_handler(msg: Message):
    await msg.answer("❗️ Iltimos, ovozli xabar (🎤) yoki audio fayl yuboring.")


# ====================== 🖼️ RASM BO'LIMI ======================

@dp.message(F.text == "Rasm 🖼️")
async def rasm_bolim_handler(msg: Message, state: FSMContext):
    await msg.answer("🖼️ Rasm bo'limi. Kerakli funksiyani tanlang:", reply_markup=rasm_menyu)
    await state.set_state("rasm_bolim")


@dp.message(StateFilter("rasm_bolim"), F.text == "⬅️ Orqaga")
async def rasm_orqaga_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Bosh menyu:", reply_markup=menyu)


@dp.message(StateFilter("rasm_bolim"), F.text.in_(RASM_FILTRLARI.keys()))
async def rasm_filtr_tanlash_handler(msg: Message, state: FSMContext):
    tanlangan_filtr = RASM_FILTRLARI[msg.text]
    await state.update_data(rasm_filtri=tanlangan_filtr)
    await msg.answer("📷 Endi rasm yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("rasm_kutish")


@dp.message(StateFilter("rasm_kutish"), F.photo)
async def rasm_qayta_ishlash_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    filtr = data.get("rasm_filtri")

    kutish = await msg.answer("⏳ Rasm qayta ishlanmoqda...")

    photo = msg.photo[-1]
    fayl = await bot.get_file(photo.file_id)
    kirish_path = f"rasm_kirish_{msg.from_user.id}.jpg"
    chiqish_path = f"rasm_chiqish_{msg.from_user.id}.png"
    await bot.download_file(fayl.file_path, kirish_path)

    try:
        if filtr == "grayscale":
            await asyncio.to_thread(oq_qora_qilish, kirish_path, chiqish_path)
            await kutish.delete()
            await msg.answer_photo(photo=FSInputFile(chiqish_path))

        elif filtr == "blur":
            await asyncio.to_thread(blur_qilish, kirish_path, chiqish_path)
            await kutish.delete()
            await msg.answer_photo(photo=FSInputFile(chiqish_path))

        elif filtr == "cartoon":
            await asyncio.to_thread(cartoon_effekt, kirish_path, chiqish_path)
            await kutish.delete()
            await msg.answer_photo(photo=FSInputFile(chiqish_path))

        elif filtr == "remove_bg":
            await asyncio.to_thread(fon_ochirish, kirish_path, chiqish_path)
            await kutish.delete()
            # Shaffoflikni saqlab qolish uchun document sifatida yuboriladi
            await msg.answer_document(document=FSInputFile(chiqish_path))

        elif filtr == "face_mesh":
            topildi = await asyncio.to_thread(yuz_mesh_filtri, kirish_path, chiqish_path)
            await kutish.delete()
            if topildi:
                await msg.answer_photo(photo=FSInputFile(chiqish_path))
            else:
                await msg.answer("❌ Rasmda yuz aniqlanmadi.")

        elif filtr == "ocr":
            matn = await asyncio.to_thread(matnni_ochirish, kirish_path)
            if matn.strip():
                await kutish.edit_text(f"📝 Topilgan matn:\n\n{matn}")
            else:
                await kutish.edit_text("❌ Rasmda matn topilmadi.")

        else:
            await kutish.delete()
            await msg.answer("❌ Noma'lum filtr tanlandi.")

    except Exception as e:
        logging.warning(f"Rasmni qayta ishlashda xatolik: {e}")
        try:
            await kutish.delete()
        except Exception:
            pass
        await msg.answer("❌ Rasmni qayta ishlashda xatolik yuz berdi.")
    finally:
        for p in (kirish_path, chiqish_path):
            if os.path.exists(p):
                os.remove(p)

    await msg.answer("Yana davom etamizmi?", reply_markup=rasm_menyu)
    await state.set_state("rasm_bolim")


@dp.message(StateFilter("rasm_kutish"))
async def rasm_notoggri_handler(msg: Message):
    await msg.answer("❗️ Iltimos, rasm (photo) ko'rinishida yuboring.")


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))