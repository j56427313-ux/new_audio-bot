import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from deep_translator import GoogleTranslator

from config import BOT_TOKEN
from states import TarjimaState
from buttons import menyu, tillar_kb
from obuna import obunani_tekshir
from middlewares import (
    SubscriptionMiddleware,
    IncomingLogMiddleware,
    OutgoingLogMiddleware,
    admin_reply_map,
)

# Windows'da aiohttp/ProactorEventLoop bilan bog'liq
# "[WinError 64] The specified network name is no longer available"
# kabi tasodifiy tarmoq xatolarini kamaytirish uchun SelectorEventLoop'ga o'tamiz.
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Tarmoq so'rovlari uchun kengroq timeout — sekin/beqaror internetda
# ulanish tez-tez uzilib qolmasligi uchun.
session = AiohttpSession(timeout=60)

bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
ADMIN = 7467403246

# 1) Avval majburiy obunani tekshiramiz (obuna bo'lmasa, boshqa hech narsa ishlamaydi)
dp.message.outer_middleware(SubscriptionMiddleware())
dp.callback_query.outer_middleware(SubscriptionMiddleware())

# 2) Faqat obunadan o'tgan (yoki admin) foydalanuvchilar uchun log middleware'lari
dp.message.outer_middleware(IncomingLogMiddleware())
dp.callback_query.outer_middleware(IncomingLogMiddleware())

# Botning barcha javoblarini (send_message, edit_text) adminga log qilish
bot.session.middleware(OutgoingLogMiddleware())


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer(
            "👨‍💻 Xush kelibsiz, Admin!\n\n"
            "Bu yerda foydalanuvchilarning botga yozgan xabarlari va botning "
            "ularga bergan javoblari sizga avtomatik yuborib turiladi.\n\n"
            "Foydalanuvchiga javob yozish uchun uning xabari haqidagi "
            "log-xabarga <b>Reply</b> qilib, matningizni yuboring — u to'g'ridan-to'g'ri "
            "o'sha foydalanuvchiga yetkaziladi.",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    # Bu yerga faqat SubscriptionMiddleware'dan o'tgan (obuna bo'lgan) foydalanuvchi yetib keladi
    await msg.answer(
        f"Assalomu aleykum {msg.from_user.full_name}, TARJIMON botimizga xush kelibsiz!"
    )
    await msg.answer(
        "Tarjima qilishni boshlash uchun pastdagi tugmani bosing:",
        reply_markup=menyu,
    )


@dp.callback_query(F.data == "check_subscription")
async def check_subscription_handler(callback: CallbackQuery):
    obuna_bolmagan = await obunani_tekshir(bot, callback.from_user.id)

    if obuna_bolmagan:
        await callback.answer(
            "❌ Siz hali barcha kanallarga obuna bo'lmadingiz. Obuna bo'lib, qayta urinib ko'ring.",
            show_alert=True,
        )
        return

    await callback.answer("✅ Obuna tasdiqlandi!")
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        f"Assalomu aleykum {callback.from_user.full_name}, TARJIMON botimizga xush kelibsiz!"
    )
    await callback.message.answer(
        "Tarjima qilishni boshlash uchun pastdagi tugmani bosing:",
        reply_markup=menyu,
    )


@dp.message(F.from_user.id == ADMIN, F.reply_to_message)
async def admin_javob_yozish(msg: Message):
    target_user_id = admin_reply_map.get(msg.reply_to_message.message_id)

    if not target_user_id:
        await msg.answer(
            "⚠️ Bu xabarga javob yuborib bo'lmaydi — foydalanuvchi topilmadi. "
            "Iltimos, foydalanuvchi haqidagi log-xabarni to'g'ridan-to'g'ri Reply qiling."
        )
        return

    try:
        await bot.send_message(target_user_id, msg.text or msg.caption or "")
        await msg.answer("✅ Xabaringiz foydalanuvchiga yuborildi.")
    except Exception:
        logging.exception("Admin javobini foydalanuvchiga yuborishda xatolik")
        await msg.answer(
            "❌ Xabar yuborilmadi. Foydalanuvchi botni bloklagan bo'lishi mumkin."
        )


@dp.message(F.text == "🌐 Tarjima qilish")
async def tarjima_qilish(msg: Message, state: FSMContext):
    await msg.answer(
        "Tarjima qilish uchun matningiz qaysi tildan bo'lishini tanlang:",
        reply_markup=tillar_kb,
    )
    await state.set_state(TarjimaState.qaysi_tildan)


@dp.callback_query(StateFilter(TarjimaState.qaysi_tildan))
async def qaysi_tildan(callback: CallbackQuery, state: FSMContext):
    await state.update_data(qaysi_tildan=callback.data)
    await callback.message.edit_text(
        "Qaysi tilga tarjima qilmoqchisiz?", reply_markup=tillar_kb
    )
    await state.set_state(TarjimaState.qaysi_tilga)
    await callback.answer()


@dp.callback_query(StateFilter(TarjimaState.qaysi_tilga))
async def qaysi_tilga(callback: CallbackQuery, state: FSMContext):
    await state.update_data(qaysi_tilga=callback.data)
    await callback.message.edit_text("Endi tarjima qilmoqchi bo'lgan matningizni yuboring:")
    await state.set_state(TarjimaState.matn)
    await callback.answer()


@dp.message(StateFilter(TarjimaState.matn))
async def matn_qabul_qilish(msg: Message, state: FSMContext):
    if not msg.text:
        await msg.answer("Iltimos, faqat matn (text) yuboring.")
        return

    data = await state.get_data()
    qaysi_tildan = data.get("qaysi_tildan")
    qaysi_tilga = data.get("qaysi_tilga")
    matn = msg.text

    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")

    try:
        tarjima_qilingan_matn = await asyncio.to_thread(
            lambda: GoogleTranslator(source=qaysi_tildan, target=qaysi_tilga).translate(matn)
        )
    except Exception as e:
        logging.exception("Tarjima qilishda xatolik")
        await msg.answer(
            "Kechirasiz, tarjima qilishda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.",
            reply_markup=menyu,
        )
        await state.clear()
        return

    await msg.answer(
        f"Tarjima qilingan matn:\n{tarjima_qilingan_matn}",
        reply_markup=menyu,
    )

    await state.clear()


async def main():
    while True:
        try:
            await dp.start_polling(bot)
        except Exception:
            logging.exception(
                "Polling kutilmaganda to'xtadi, 5 soniyadan keyin qayta ishga tushirilmoqda..."
            )
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())