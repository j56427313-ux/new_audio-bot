"""
Media Downloader Telegram Bot
------------------------------
- Foydalanuvchi Instagram / YouTube / TikTok / Twitter va h.k. link yuborsa,
  bot videoni yoki undagi musiqani (mp3) yuklab beradi.
- Barcha foydalanuvchi xabarlari adminga forward qilinadi.
- Admin forward qilingan xabarga "Reply" qilib javob yozsa,
  javob avtomatik o'sha foydalanuvchiga yuboriladi.
- Admin /reply <user_id> <matn> buyrug'i orqali ham xabar yozishi mumkin.

Fayllar:
    config.py   -> BOT_TOKEN, ADMIN_ID va boshqa sozlamalar
    states.py   -> vaqtinchalik xotira (forward_map, pending_links)
    buttons.py  -> inline tugmalar
    bot.py      -> shu fayl, asosiy dastur

O'rnatish va sozlash uchun README.md faylini o'qing.
"""

import os
import re
import logging
import asyncio
import shutil

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import yt_dlp

from config import BOT_TOKEN, ADMIN_ID, DOWNLOAD_DIR, MAX_FILE_SIZE_MB
from buttons import download_choice_keyboard
import states

# ---------------------------------------------------------------------------
# SOZLAMALAR
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

URL_REGEX = re.compile(r"https?://\S+")


# ---------------------------------------------------------------------------
# ASOSIY BUYRUQLAR
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        text = (
            "🛠 Xush kelibsiz, Admin!\n\n"
            "Bu — botning boshqaruv rejimi. Bu yerda video/musiqa yuklash "
            "funksiyasi ishlamaydi, chunki siz admin sifatida tanildingiz.\n\n"
            "📥 Foydalanuvchilar yozgan barcha xabarlar sizga shu yerga forward "
            "bo'lib keladi.\n"
            "↩️ Javob berish uchun forward qilingan xabarga Reply qiling\n"
            "✍️ Yoki: /reply <user_id> <matn>\n\n"
            "Botni oddiy foydalanuvchi sifatida sinab ko'rish uchun boshqa "
            "Telegram akkaunt (yoki do'stingiz) orqali oching."
        )
        await update.message.reply_text(text)
        return

    text = (
        "Salom! 👋\n\n"
        "Menga Instagram, YouTube, TikTok yoki boshqa saytdan video havolasini "
        "(link) yuboring — men sizga videoni yoki undagi musiqani (mp3) "
        "yuklab beraman.\n\n"
        "Shunchaki link yuboring va keyin 🎥 Video yoki 🎵 Musiqa tugmasini tanlang."
    )
    await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Foydalanish tartibi:\n"
        "1. Video havolasini yuboring (Instagram, YouTube, TikTok...)\n"
        "2. 🎥 Video yoki 🎵 Musiqa tugmasini bosing\n"
        "3. Bot faylni yuklab, sizga jo'natadi\n\n"
        "Savol yoki taklif bo'lsa, shu botga xabar yozing — admin javob beradi."
    )


# ---------------------------------------------------------------------------
# YUKLAB OLISH (yt-dlp) — TEZLIK UCHUN OPTIMALLASHTIRILGAN
# ---------------------------------------------------------------------------

# Agar tizimda aria2c o'rnatilgan bo'lsa, undan foydalanamiz — u bir nechta
# ulanish orqali (multi-connection) yuklaydi va odatiy yuklashdan 2-5 baravar
# tezroq ishlaydi. Bo'lmasa, yt-dlp o'zining standart yuklovchisidan foydalanadi.
_ARIA2C_AVAILABLE = shutil.which("aria2c") is not None

_COMMON_OPTS = {
    "quiet": True,
    "noplaylist": True,
    "noprogress": True,
    "concurrent_fragment_downloads": 8,   # HLS/DASH fragmentlarini parallel yuklash
    "retries": 3,
    "fragment_retries": 3,
    "socket_timeout": 15,
    "geo_bypass": True,
    "nocheckcertificate": True,
}

if _ARIA2C_AVAILABLE:
    _COMMON_OPTS.update(
        {
            "external_downloader": "aria2c",
            "external_downloader_args": {
                # -x16: 16 tagacha ulanish, -s16: faylni 16 qismga bo'lib yuklash,
                # -k1M: har bir qism kamida 1MB — juda kichik fayllarda xato bermaydi
                "aria2c": ["-x", "16", "-s", "16", "-k", "1M"]
            },
        }
    )


def build_ydl_opts(mode: str, out_template: str) -> dict:
    opts = dict(_COMMON_OPTS)
    opts["outtmpl"] = out_template

    if mode == "audio":
        opts.update(
            {
                # to'g'ridan-to'g'ri audio formatini olamiz — video oqimini
                # yuklamaymiz, shuning uchun ancha tez va tejamli
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        opts.update(
            {
                # 720p bilan cheklaymiz: fayl hajmi kichikroq bo'ladi ->
                # ham yuklash, ham Telegram'ga yuborish tezlashadi.
                # Progressiv (allaqachon birlashtirilgan) mp4 bo'lsa uni
                # olamiz — merge qilish shart bo'lmaydi, bu ham vaqt tejaydi.
                "format": (
                    "best[ext=mp4][height<=720]/"
                    "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/"
                    "best[height<=720]/best"
                ),
                "merge_output_format": "mp4",
            }
        )
    return opts


def download_media(url: str, ydl_opts: dict, mode: str) -> str:
    """Sinxron (blocking) funksiya — alohida thread'da ishlaydi."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if mode == "audio":
            base, _ = os.path.splitext(filename)
            filename = base + ".mp3"
        return filename


# ---------------------------------------------------------------------------
# ADMIN BILAN XABARLASHISH
# ---------------------------------------------------------------------------
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi yozgan har qanday xabarni (matn, rasm, video...) adminga forward qiladi."""
    if ADMIN_ID == 0 or update.effective_user.id == ADMIN_ID:
        return
    user = update.effective_user
    try:
        fwd = await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )
        states.save_forward(fwd.message_id, user.id)

        info = (
            f"👤 {user.full_name} (@{user.username or '—'})\n"
            f"🆔 ID: {user.id}\n"
            f"↩️ Javob berish uchun shu xabarlarga Reply qiling "
            f"yoki: /reply {user.id} matn"
        )
        info_msg = await context.bot.send_message(chat_id=ADMIN_ID, text=info)
        states.save_forward(info_msg.message_id, user.id)
    except Exception as e:
        logger.error("Adminga forward qilishda xato: %s", e)


async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/reply <user_id> <matn> — admin foydalanuvchiga to'g'ridan-to'g'ri yozadi."""
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Foydalanish: /reply <user_id> <xabar matni>")
        return
    try:
        user_id = int(args[0])
    except ValueError:
        await update.message.reply_text("user_id raqam bo'lishi kerak.")
        return
    text = " ".join(args[1:])
    try:
        await context.bot.send_message(chat_id=user_id, text=f"👨‍💼 Admin: {text}")
        await update.message.reply_text("✅ Yuborildi.")
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")


# ---------------------------------------------------------------------------
# XABARLARNI QAYTA ISHLASH
# ---------------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text or update.message.caption or ""

    # 1) Admin forward qilingan xabarga Reply qilgan bo'lsa
    if (
        update.effective_user.id == ADMIN_ID
        and update.message.reply_to_message
        and text
    ):
        replied_id = update.message.reply_to_message.message_id
        target_user_id = states.get_user_by_forward(replied_id)
        if target_user_id:
            try:
                await context.bot.send_message(
                    chat_id=target_user_id, text=f"👨‍💼 Admin: {text}"
                )
                await update.message.reply_text("✅ Xabar foydalanuvchiga yuborildi.")
            except Exception as e:
                await update.message.reply_text(f"❌ Xatolik: {e}")
            return

    # 2) Oddiy foydalanuvchi xabari bo'lsa — adminga forward qilamiz
    await forward_to_admin(update, context)

    if update.effective_user.id == ADMIN_ID:
        # Admin uchun video/musiqa tugmalari chiqmaydi — buni tushuntiramiz,
        # jim qolib foydalanuvchini chalkashtirmaslik uchun.
        if URL_REGEX.search(text):
            await update.message.reply_text(
                "ℹ️ Siz admin sifatida tanildingiz — video/musiqa yuklash "
                "funksiyasi faqat oddiy foydalanuvchilar uchun ishlaydi.\n\n"
                "Buni sinab ko'rish uchun boshqa Telegram akkaunt orqali botga "
                "yozing. Foydalanuvchilar bilan gaplashish uchun ularning "
                "forward qilingan xabariga Reply qiling yoki /reply buyrug'idan "
                "foydalaning."
            )
        return

    # 3) Xabarda link bo'lsa — video/audio tanlash tugmalarini chiqaramiz
    url_match = URL_REGEX.search(text)
    if url_match:
        url = url_match.group(0)
        states.save_pending_link(update.effective_chat.id, url)
        await update.message.reply_text(
            "Nimani yuklab beray?", reply_markup=download_choice_keyboard()
        )
    elif text:
        await update.message.reply_text(
            "Iltimos, menga video havolasini (Instagram, YouTube, TikTok va h.k.) yuboring."
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    url = states.get_pending_link(chat_id)
    if not url:
        await query.edit_message_text("❗️ Havola topilmadi. Iltimos, linkni qayta yuboring.")
        return

    mode = "audio" if query.data == "dl_audio" else "video"
    await query.edit_message_text("⏳ Yuklab olinmoqda, biroz kuting...")

    await context.bot.send_chat_action(
        chat_id=chat_id,
        action=ChatAction.UPLOAD_DOCUMENT if mode == "audio" else ChatAction.UPLOAD_VIDEO,
    )

    out_template = os.path.join(DOWNLOAD_DIR, f"{chat_id}_%(id)s.%(ext)s")
    ydl_opts = build_ydl_opts(mode, out_template)

    loop = asyncio.get_event_loop()
    try:
        filepath = await loop.run_in_executor(
            None, lambda: download_media(url, ydl_opts, mode)
        )
    except Exception as e:
        logger.error("Yuklashda xato: %s", e)
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Yuklab bo'lmadi: {e}")
        return

    if not filepath or not os.path.exists(filepath):
        await context.bot.send_message(chat_id=chat_id, text="❌ Fayl topilmadi, qayta urinib ko'ring.")
        return

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ Fayl juda katta ({size_mb:.1f}MB). "
            f"Oddiy Telegram bot orqali {MAX_FILE_SIZE_MB}MB dan katta fayl yuborib bo'lmaydi.",
        )
        os.remove(filepath)
        return

    try:
        with open(filepath, "rb") as f:
            if mode == "audio":
                await context.bot.send_audio(chat_id=chat_id, audio=f)
            else:
                await context.bot.send_video(chat_id=chat_id, video=f, supports_streaming=True)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
        states.clear_pending_link(chat_id)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Barcha kutilmagan xatolarni ushlab, to'liq traceback o'rniga qisqa
    log yozadi. Tarmoq (internet/DNS) xatolari odatda vaqtinchalik bo'ladi —
    kutubxona o'zi avtomatik qayta urinadi, shuning uchun bot ishlashda
    davom etaveradi."""
    logger.warning("Kutilmagan xatolik: %s", context.error)


# ---------------------------------------------------------------------------
# ISHGA TUSHIRISH
# ---------------------------------------------------------------------------
def main():
    if BOT_TOKEN == "SIZNING_BOT_TOKENINGIZ_BU_YERGA" or ADMIN_ID == 0:
        logger.warning(
            "BOT_TOKEN yoki ADMIN_ID sozlanmagan! config.py faylini to'ldiring."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    if _ARIA2C_AVAILABLE:
        logger.info("aria2c topildi — tez (multi-connection) yuklash yoqilgan.")
    else:
        logger.info(
            "aria2c topilmadi — standart yuklash ishlatiladi. "
            "Tezlashtirish uchun: winget install aria2 (Windows) "
            "yoki sudo apt install aria2 (Linux)."
        )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reply", reply_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()