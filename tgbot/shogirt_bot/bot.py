import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from config import TOKEN, ADMIN_ID, CHANNEL_ID
from buttons import main_menu, orqaga_menu, telefon_button, admin_tasdiqlash_keyboard
from states import ElonStates

router = Router()

pending_elonlar: dict[int, dict] = {}

TUGMALAR = {
    "🤝 Sherik kerak":   "Sherik",
    "🏢 Ish joyi kerak": "Ish joyi",
    "👔 Hodim kerak":    "Hodim",
    "👨‍🏫 Ustoz kerak":   "Ustoz",
}


# ===================== YORDAMCHI FUNKSIYALAR =====================

async def so_ra_ism(message: Message):
    await message.answer(
        "Ism va familyangizni yozing (masalan: Alisher Karimov):",
        reply_markup=orqaga_menu()
    )

async def so_ra_kasb(message: Message):
    await message.answer(
        "Kerakli kasbni yozing (masalan: Dasturchi, Buxgalter, Menejer):",
        reply_markup=orqaga_menu()
    )

async def so_ra_texnologiya(message: Message):
    await message.answer(
        "📚 <b>Texnologiya:</b>\n\n"
        "Talab qilinadigan texnologiyalarni kiriting.\n"
        "Texnologiya nomlarini vergul bilan ajrating. Masalan:\n\n"
        "<i>Java, C++, C#</i>",
        reply_markup=orqaga_menu()
    )

async def so_ra_davlat(message: Message):
    await message.answer(
        "Qaysi <b>davlatda</b> ish kerakligini yozing (masalan: O'zbekiston, Rossiya, Koreya):",
        reply_markup=orqaga_menu()
    )

async def so_ra_ish_haqi(message: Message):
    await message.answer(
        "<b>Ish haqini</b> kiriting (masalan: 3 000 000 so'm yoki 500$):",
        reply_markup=orqaga_menu()
    )

async def so_ra_telefon(message: Message):
    await message.answer(
        "Telefon raqamingizni yuborish uchun pastdagi tugmani bosing 👇",
        reply_markup=telefon_button()
    )


# ===================== /start =====================

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! 👋\nBotdan foydalanish uchun kerakli bo'limni tanlang:",
        reply_markup=main_menu()
    )


# ===================== ASOSIY 4 TUGMA =====================

@router.message(F.text.in_(TUGMALAR.keys()))
async def tur_tanlandi(message: Message, state: FSMContext):
    turi = TUGMALAR[message.text]
    await state.update_data(turi=turi)
    await so_ra_ism(message)
    await state.set_state(ElonStates.ism_familya_kutilyapti)


# ===================== ORQAGA TUGMASI =====================

@router.message(F.text == "⬅️ Orqaga")
async def orqaga_handler(message: Message, state: FSMContext):
    joriy_holat = await state.get_state()

    # Ism familya -> Bosh menyu
    if joriy_holat == ElonStates.ism_familya_kutilyapti:
        await state.clear()
        await message.answer(
            "Bosh menyuga qaytdingiz 👇",
            reply_markup=main_menu()
        )

    # Kasb -> Ism familya
    elif joriy_holat == ElonStates.kasb_kutilyapti:
        await so_ra_ism(message)
        await state.set_state(ElonStates.ism_familya_kutilyapti)

    # Texnologiya -> Kasb
    elif joriy_holat == ElonStates.texnologiya_kutilyapti:
        await so_ra_kasb(message)
        await state.set_state(ElonStates.kasb_kutilyapti)

    # Davlat -> Texnologiya
    elif joriy_holat == ElonStates.davlat_kutilyapti:
        await so_ra_texnologiya(message)
        await state.set_state(ElonStates.texnologiya_kutilyapti)

    # Ish haqi -> Davlat
    elif joriy_holat == ElonStates.ish_haqi_kutilyapti:
        await so_ra_davlat(message)
        await state.set_state(ElonStates.davlat_kutilyapti)

    # Telefon -> Ish haqi
    elif joriy_holat == ElonStates.telefon_kutilyapti:
        await so_ra_ish_haqi(message)
        await state.set_state(ElonStates.ish_haqi_kutilyapti)

    # Boshqa holat -> Bosh menyu
    else:
        await state.clear()
        await message.answer(
            "Bosh menyuga qaytdingiz 👇",
            reply_markup=main_menu()
        )


# ===================== SO'ROVNOMA BOSQICHLARI =====================

# 1. Ism familya -> Kasb
@router.message(ElonStates.ism_familya_kutilyapti)
async def ism_familya_qabul_qilish(message: Message, state: FSMContext):
    await state.update_data(ism_familya=message.text)
    await so_ra_kasb(message)
    await state.set_state(ElonStates.kasb_kutilyapti)


# 2. Kasb -> Texnologiya
@router.message(ElonStates.kasb_kutilyapti)
async def kasb_qabul_qilish(message: Message, state: FSMContext):
    await state.update_data(kasb=message.text)
    await so_ra_texnologiya(message)
    await state.set_state(ElonStates.texnologiya_kutilyapti)


# 3. Texnologiya -> Davlat
@router.message(ElonStates.texnologiya_kutilyapti)
async def texnologiya_qabul_qilish(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await so_ra_davlat(message)
    await state.set_state(ElonStates.davlat_kutilyapti)


# 4. Davlat -> Ish haqi
@router.message(ElonStates.davlat_kutilyapti)
async def davlat_qabul_qilish(message: Message, state: FSMContext):
    await state.update_data(davlat=message.text)
    await so_ra_ish_haqi(message)
    await state.set_state(ElonStates.ish_haqi_kutilyapti)


# 5. Ish haqi -> Telefon
@router.message(ElonStates.ish_haqi_kutilyapti)
async def ish_haqi_qabul_qilish(message: Message, state: FSMContext):
    await state.update_data(ish_haqi=message.text)
    await so_ra_telefon(message)
    await state.set_state(ElonStates.telefon_kutilyapti)


# 6. Telefon -> Adminga yuborish
@router.message(StateFilter(ElonStates.telefon_kutilyapti))
async def telefon_qabul_qilish(message: Message, state: FSMContext, bot: Bot):
    if message.contact is None:
        await message.answer(
            "Iltimos, telefon raqamingizni faqat «📱 Raqamni yuborish» tugmasi orqali yuboring!",
            reply_markup=telefon_button()
        )
        return

    telefon = message.contact.phone_number
    data = await state.get_data()
    await state.clear()

    turi        = data.get("turi", "-")
    ism_familya = data.get("ism_familya", "-")
    kasb        = data.get("kasb", "-")
    texnologiya = data.get("texnologiya", "-")
    davlat      = data.get("davlat", "-")
    ish_haqi    = data.get("ish_haqi", "-")

    user = message.from_user
    username = f"@{user.username}" if user.username else "username yo'q"

    elon_matni = (
        "🆕 <b>Yangi e'lon (tasdiq kutilmoqda)</b>\n\n"
        f"📌 Turi: {turi}\n"
        f"👤 Ism Familya: {ism_familya}\n"
        f"💼 Kasb: {kasb}\n"
        f"📚 Texnologiya: {texnologiya}\n"
        f"🌍 Davlat: {davlat}\n"
        f"💰 Ish haqi: {ish_haqi}\n"
        f"📞 Telefon: {telefon}\n\n"
        f"🔗 Telegram: {username}\n"
        f"🆔 ID: <code>{user.id}</code>"
    )

    pending_elonlar[user.id] = {
        "turi": turi,
        "ism_familya": ism_familya,
        "kasb": kasb,
        "texnologiya": texnologiya,
        "davlat": davlat,
        "ish_haqi": ish_haqi,
        "telefon": telefon,
        "username": username,
    }

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=elon_matni,
        reply_markup=admin_tasdiqlash_keyboard(user.id)
    )

    await message.answer(
        "✅ <b>Arizangiz qabul qilindi!</b>\n\n"
        "Ma'lumotlaringiz tekshiruvdan o'tkazilmoqda. "
        "Admin tasdiqlasa, e'loningiz kanalga joylanadi.",
        reply_markup=main_menu()
    )


# ===================== ADMIN TASDIQLASH / RAD ETISH =====================

@router.callback_query(F.data.startswith("tasdiqlash:"))
async def tasdiqlash_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Bu tugma faqat admin uchun!", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])
    elon = pending_elonlar.get(user_id)

    if not elon:
        await callback.answer("Bu e'lon allaqachon ko'rib chiqilgan.", show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        return

    kanal_matni = (
        f"📢 <b>{elon['turi']} kerak!</b>\n\n"
        f"👤 Ism Familya: {elon['ism_familya']}\n"
        f"💼 Kasb: {elon['kasb']}\n"
        f"📚 Texnologiya: {elon['texnologiya']}\n"
        f"🌍 Davlat: {elon['davlat']}\n"
        f"💰 Ish haqi: {elon['ish_haqi']}\n"
        f"📞 Telefon: {elon['telefon']}\n\n"
        f"🔗 Murojaat: {elon['username']}"
    )

    await bot.send_message(chat_id=CHANNEL_ID, text=kanal_matni)
    await bot.send_message(
        chat_id=user_id,
        text="🎉 Tabriklaymiz! E'loningiz tasdiqlandi va kanalga joylandi."
    )
    await callback.message.edit_text(
        callback.message.html_text + "\n\n✅ <b>TASDIQLANDI VA KANALGA JOYLANDI</b>",
        reply_markup=None
    )
    await callback.answer("Kanalga joylandi ✅")
    del pending_elonlar[user_id]


@router.callback_query(F.data.startswith("radetish:"))
async def radetish_handler(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Bu tugma faqat admin uchun!", show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])
    elon = pending_elonlar.get(user_id)

    if not elon:
        await callback.answer("Bu e'lon allaqachon ko'rib chiqilgan.", show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        return

    await bot.send_message(
        chat_id=user_id,
        text="❌ Afsuski, e'loningiz rad etildi. Ma'lumotlaringizni tekshirib, qaytadan urinib ko'ring."
    )
    await callback.message.edit_text(
        callback.message.html_text + "\n\n❌ <b>RAD ETILDI</b>",
        reply_markup=None
    )
    await callback.answer("Rad etildi ❌")
    del pending_elonlar[user_id]


# ===================== BOSHQA XABARLAR =====================

@router.message()
async def boshqa_xabarlar(message: Message):
    await message.answer(
        "Iltimos, quyidagi menyudan birini tanlang 👇",
        reply_markup=main_menu()
    )


# ===================== ISHGA TUSHIRISH =====================

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())