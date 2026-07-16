import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command

# =================================================================
# 1. BOT SOZLAMALARI VA MA'LUMOTLAR BAZASI
# =================================================================

# BOT TOKEN VA ADMIN ID NI SHU YERGA YOZING
BOT_TOKEN = "8991161080:AAE5KBufaPiBNuXo0r86Uo26KgP-ZhzemNE"
ADMIN_ID = 7467403246 # Sizning Telegram ID'ngiz o'rnatildi

# 📣 MAJBURIY OBUNA KANALLARI SOZLAMALARI
# Kerakli miqdorda kanal/chat qo'shishingiz mumkin — har biriga "id" (chat_id yoki @username),
# "url" (a'zo bo'lish uchun link) va "name" (tugma matnida ko'rinadigan nom) kiriting.
MANDATORY_CHANNELS = [
    {"id": "@mars_auto_bot", "url": "https://t.me/muzikalar_uzmuz_aslmuzik", "name": "Mars Auto"},
    
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

USERS_DATA = {}

# HAQIQIY RASMLAR LINKI BILAN YANGILANGAN MAHSULOTLAR RO'YXATI
PRODUCTS_INFO = {
    "🎒 Mars Ryukzak": {"id": "ryukzak", "price": 150, "desc": "Sifatli va qulay Mars ryukzaki.", "img": "https://lab.marsit.uz/media/shop/Mars%20Backpack/backpack.png"},
    "👕 Mars Huddi": {"id": "huddi", "price": 200, "desc": "Issiq va zamonaviy Mars hudditi.", "img": "https://lab.marsit.uz/media/shop/Branded%20Hoodie/1be3f684-6bbb-4340-8a07-c59581d19c5d-0.png"},
    "🧢 Mars Kepka": {"id": "kepka", "price": 50, "desc": "Quyoshdan himoya qiluvchi Mars kepkasi.", "img": "https://lab.marsit.uz/media/shop/Branded%20Cap/kepka_mars-removebg-preview.png"},
    "📔 Mars Bloknot": {"id": "bloknot", "price": 30, "desc": "G'oyalaringizni yozib borish uchun bloknot.", "img": "https://lab.marsit.uz/media/shop/Notepad/mars_it_schoool-removebg-preview.png"},
    "🥤 Mars Termos": {"id": "termos", "price": 80, "desc": "Ichimlikni issiq saqlovchi qulay termos.", "img": "https://lab.marsit.uz/media/shop/Branded%20Thermos/termos_mars-removebg-preview.png"},
    "🖱️ Mars Kovrik": {"id": "kovrik", "price": 40, "desc": "Silliq harakatlanuvchi sichqoncha kovriki.", "img": "https://lab.marsit.uz/media/shop/Mouse/mouse_compressed.png"},
    "🎧 Mars Naushnik": {"id": "naushnik", "price": 250, "desc": "Tiniq ovozli Mars quloqchinlari.", "img": "https://lab.marsit.uz/media/shop/AirPods%20Max/Shop_AirPodsmax-removebg-preview.png"},
    "🔌 Powerbank": {"id": "power", "price": 180, "desc": "Telefoningiz uchun quvvatlantirgich.", "img": "https://lab.marsit.uz/media/shop/Branded%20Powerbank/branded_powerband.png"},
    "⌨️ Klaviatura": {"id": "klava", "price": 300, "desc": "Mexanik Mars o'yin klaviaturasi.", "img": "https://lab.marsit.uz/media/shop/Keyboard&mouse/keyboard__mouse_compressed.png"},
    "🖊️ Mars Ruchka": {"id": "ruchka", "price": 10, "desc": "Mars IT logotipli ajoyib ruchka.", "img": "https://lab.marsit.uz/media/shop/Mars%20pen/sensor_ruchka_mars-removebg-preview.png"},
}

# =================================================================
# 1.1 STIKERLAR SOZLAMASI
# =================================================================
# Har bir voqea uchun stiker file_id.
# Haqiqiy file_id olish uchun: istalgan stikerni @userinfobot yoki
# @RawDataBot ga forward qiling — javobida "file_id" ko'rinadi, shuni nusxalab
# pastdagi qiymatlarga qo'ying. Bo'sh/placeholder qoldirilsa, bot xato bermay
# shunchaki stiker yubormay o'tib ketadi.
STICKERS = {
    "welcome": "",    # Tizimga muvaffaqiyatli kirganda
    "purchase": "",   # Mahsulot muvaffaqiyatli sotib olinganda
    "feedback": "",   # Izoh adminga yuborilganda
}


async def send_sticker_safe(chat_id: int, key: str) -> None:
    """STICKERS lug'atidan stiker yuboradi; bo'sh yoki xato bo'lsa botni to'xtatmaydi."""
    sticker_id = STICKERS.get(key)
    if not sticker_id:
        return
    try:
        await bot.send_sticker(chat_id=chat_id, sticker=sticker_id)
    except Exception as e:
        logging.warning(f"Stiker yuborilmadi ({key}): {e}")




def get_subscribe_keyboard():
    builder = InlineKeyboardBuilder()
    for ch in MANDATORY_CHANNELS:
        builder.row(InlineKeyboardButton(text=f"➕ {ch['name']}", url=ch["url"]))
    builder.row(InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription"))
    return builder.as_markup()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Profil"), KeyboardButton(text="🪙 Coin")],
        [KeyboardButton(text="🚀 Space shop"), KeyboardButton(text="🏫 Maktab haqida")],
        [KeyboardButton(text="✍️ Izoh qoldirish")]
    ],
    resize_keyboard=True
)

def get_shop_keyboard():
    builder = ReplyKeyboardBuilder()
    for product in PRODUCTS_INFO.keys():
        builder.add(KeyboardButton(text=product))
    builder.adjust(2)
    builder.row(KeyboardButton(text="⬅️ Bosh menyuga qaytish"))
    return builder.as_markup(resize_keyboard=True)

def get_buy_inline_keyboard(product_id: str):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Sotib olish 🛒", callback_data=f"buy_{product_id}"),
        InlineKeyboardButton(text="Yo'q ❌", callback_data="cancel_buy")
    )
    return builder.as_markup()

def get_admin_reply_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="✍️ Javob yozish", 
        callback_data=f"reply_{user_id}"
    ))
    return builder.as_markup()

cancel_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True
)

# =================================================================
# 3. YORDAMCHI FUNKSIYA (OBUNANI TEKSHIRISH)
# =================================================================

async def check_user_subscription(user_id: int) -> bool:
    """Foydalanuvchi MANDATORY_CHANNELS ro'yxatidagi BARCHA kanallarga a'zo ekanini tekshiradi."""
    for ch in MANDATORY_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except Exception as e:
            logging.warning(f"Obuna tekshirishda xatolik ({ch['id']}): {e}")
            return False
    return True

# =================================================================
# 4. FSM (HOLATLAR) VA MANTIQ SEKSIYASI
# =================================================================

class BotStates(StatesGroup):
    login = State()
    password = State()
    waiting_for_feedback = State()
    admin_waiting_reply = State()

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    
    is_subscribed = await check_user_subscription(user_id)
    
    if is_subscribed:
        await message.answer("🤖 Mars IT Botga xush kelibsiz!\n\nTizimga kirish uchun **Login**ingizni kiriting:")
        await state.set_state(BotStates.login)
    else:
        await message.answer(
            "⚠️ **Botdan foydalanish uchun birinchi navbatda rasmiy kanalimizga obuna bo'lishingiz shart!**", 
            reply_markup=get_subscribe_keyboard()
        )

@dp.callback_query(F.data == "check_subscription")
async def process_check_subscription(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    is_subscribed = await check_user_subscription(user_id)
    
    if is_subscribed:
        await callback.message.delete()
        await callback.message.answer("✅ Rahmat! Obuna tasdiqlandi.\n\nTizimga kirish uchun **Login**ingizni kiriting:")
        await state.set_state(BotStates.login)
        await callback.answer("Muvaffaqiyatli o'tildi!", show_alert=False)
    else:
        await callback.answer("❌ Uzr, siz hali kanalga obuna bo'lmagansiz! Qayta urinib ko'ring.", show_alert=True)

@dp.message(BotStates.login)
async def process_login(message: Message, state: FSMContext):
    if message.text == "mars123":
        await state.update_data(login=message.text)
        await message.answer("Parolingizni kiriting:")
        await state.set_state(BotStates.password)
    else:
        await message.answer("❌ Login noto'g'ri. Qaytadan urinib ko'ring:")

@dp.message(BotStates.password)
async def process_password(message: Message, state: FSMContext):
    if message.text == "1234":
        user_id = message.from_user.id
        if user_id not in USERS_DATA:
            USERS_DATA[user_id] = {
                "ism": message.from_user.first_name,
                "familiya": message.from_user.last_name or "Kiritilmagan",
                "guruh": "Beckend",
                "coins": 500  
            }
        await message.answer("✅ Tizimga muvaffaqiyatli kirdingiz!", reply_markup=main_menu)
        await send_sticker_safe(user_id, "welcome")
        await state.clear()
    else:
        await message.answer("❌ Parol noto'g'ri. Qaytadan kiriting:")

@dp.message(F.text == "⬅️ Bosh menyuga qaytish")
async def back_to_main(message: Message):
    await message.answer("Siz bosh menyuga qaytdingiz.", reply_markup=main_menu)

@dp.message(F.text == "👤 Profil")
async def show_profile(message: Message):
    u = USERS_DATA.get(message.from_user.id, {"ism": "Noma'lum", "familiya": "-", "guruh": "-", "coins": 0})
    text = (f"👤 **Sizning profilingiz:**\n\n"
            f"Ism: {u['ism']}\n"
            f"Familiya: {u['familiya']}\n"
            f"Guruh: {u['guruh']}\n"
            f"ID: `{message.from_user.id}`")
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🪙 Coin")
async def show_coins(message: Message):
    u = USERS_DATA.get(message.from_user.id, {"coins": 0})
    await message.answer(f"🪙 Hozirgi hisobingizda: **{u['coins']} Mars Coin** bor.", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text == "🚀 Space shop")
async def show_shop(message: Message):
    text = "🛍️ **Space Shop do'koniga xush kelibsiz!**\n\n🌐 Sayt orqali ko'rish: [Mars Space Shop](https://landing.marsit.uz/)\n\nQuyidagi tugmalardan mahsulotni tanlang:"
    await message.answer(text, reply_markup=get_shop_keyboard(), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@dp.message(lambda msg: msg.text in PRODUCTS_INFO.keys())
async def preview_product(message: Message):
    prod_name = message.text
    product = PRODUCTS_INFO[prod_name]
    caption = (f"🎁 **{prod_name}**\n\n"
               f"📝 {product['desc']}\n"
               f"💰 Narxi: {product['price']} Coin\n\n"
               f"❓ Ushbu mahsulotni sotib olasizmi?")
    try:
        await message.answer_photo(
            photo=URLInputFile(product['img']),
            caption=caption,
            reply_markup=get_buy_inline_keyboard(product['id']),
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        # Rasm yuklanmasa (link ishlamay qolsa) ham foydalanuvchi xaridni davom ettira oladi
        logging.warning(f"Mahsulot rasmi yuklanmadi ({prod_name}): {e}")
        await message.answer(
            f"⚠️ Rasm hozircha yuklanmadi.\n\n{caption}",
            reply_markup=get_buy_inline_keyboard(product['id']),
            parse_mode=ParseMode.MARKDOWN,
        )

@dp.callback_query(F.data.startswith("buy_"))
async def confirm_purchase(callback: CallbackQuery):
    user_id = callback.from_user.id
    prod_id = callback.data.split("_")[1]
    
    prod_name = None
    for name, info in PRODUCTS_INFO.items():
        if info["id"] == prod_id:
            prod_name = name
            break

    if user_id not in USERS_DATA:
        await callback.answer("Iltimos, botni qayta ishga tushiring /start", show_alert=True)
        return

    product = PRODUCTS_INFO[prod_name]
    user_coins = USERS_DATA[user_id]["coins"]

    if user_coins >= product["price"]:
        USERS_DATA[user_id]["coins"] -= product["price"]
        new_balance = USERS_DATA[user_id]["coins"]
        new_caption = (f"🎁 **{prod_name}**\n\n"
                       f"🎉 **Siz ushbu mahsulotni oldingiz, tabriklayman!**\n"
                       f"📉 Qoldiq balansingiz: {new_balance} Coin")
        await callback.message.edit_caption(caption=new_caption, parse_mode=ParseMode.MARKDOWN)
        await callback.answer("Muvaffaqiyatli sotib olindi! 🎉")
        await send_sticker_safe(user_id, "purchase")
    else:
        new_caption = (f"🎁 **{prod_name}**\n\n"
                       f"❌ **Kechirasiz, sizning coiningiz yetarli emas.**\n"
                       f"👨‍💻 Hisobingizni to'ldirish uchun adminga murojaat qilindi.")
        await callback.message.edit_caption(caption=new_caption, parse_mode=ParseMode.MARKDOWN)
        
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚠️ **Coin yetishmovchiligi!**\n\n"
                 f"👤 Foydalanuvchi: {callback.from_user.full_name}\n"
                 f"🆔 ID: `{user_id}`\n"
                 f"🛍️ Mahsulot: {prod_name}\n"
                 f"💰 Narxi: {product['price']} Coin\n"
                 f"📉 Hozirgi balansi: {user_coins} Coin\n\n"
                 f"Coin qo'shish uchun: `/plus {user_id} 100` shaklida yozing.",
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer("Coiningiz yetarli emas! Adminga xabar yuborildi.", show_alert=True)

@dp.callback_query(F.data == "cancel_buy")
async def cancel_purchase(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Xarid bekor qilindi.")

# 🎬 Maktab haqidagi video (o'zingizning video faylingiz manzili yoki Telegram file_id bilan almashtiring)
SCHOOL_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4"

@dp.message(F.text == "🏫 Maktab haqida")
async def show_school_info(message: Message):
    caption = ("🏫 **Mars IT Academy**\n\n"
               "Zamonaviy kasblarni mukammal o'rgatuvchi va kelajak muhandislarini "
               "tayyorlovchi akademiya.\n\n"
               "📍 Manzil: Toshkent shahar\n"
               "🌐 Sayt: https://marsit.uz")
    try:
        await message.answer_video(
            video=URLInputFile(SCHOOL_VIDEO_URL),
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        # Video yuklanmasa ham foydalanuvchi matnli ma'lumotni oladi
        logging.warning(f"Maktab video yuklanmadi: {e}")
        await message.answer(
            f"{caption}\n\n🎬 Video: {SCHOOL_VIDEO_URL}",
            parse_mode=ParseMode.MARKDOWN,
        )

# --- Izoh qoldirish ---
@dp.message(F.text == "✍️ Izoh qoldirish")
async def feedback_start(message: Message, state: FSMContext):
    await message.answer("✍️ Adminga yubormoqchi bo'lgan izohingizni kiriting (Matn yoki Rasm shaklida):", reply_markup=cancel_menu)
    await state.set_state(BotStates.waiting_for_feedback)

@dp.message(BotStates.waiting_for_feedback, F.text == "❌ Bekor qilish")
async def feedback_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Izoh qoldirish bekor qilindi.", reply_markup=main_menu)

@dp.message(BotStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    admin_text = f"📩 **Yangi izoh keldi!**\n👤 Kimdan: {user_name} (ID: `{user_id}`)\n\n"
    
    if message.text:
        admin_text += f"💬 Izoh matni:\n{message.text}"
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text, reply_markup=get_admin_reply_keyboard(user_id), parse_mode=ParseMode.MARKDOWN)
    elif message.photo:
        caption = admin_text + f"💬 Izoh rasm tagidagi matn: {message.caption or 'Mavjud emas'}"
        await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=caption, reply_markup=get_admin_reply_keyboard(user_id), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("❌ Iltimos, faqat rasm yoki matn ko'rinishida yuboring.")
        return

    await message.answer("✅ Izohingiz adminga muvaffaqiyatli yetkazildi!", reply_markup=main_menu)
    await send_sticker_safe(user_id, "feedback")
    await state.clear()

# =================================================================
# 5. ADMIN FUNKSIYALARI (JAVOB BERISH VA COIN QO'SHISH)
# =================================================================

@dp.message(Command("plus"))
async def admin_add_coins(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        if target_id not in USERS_DATA:
            USERS_DATA[target_id] = {"ism": "O'quvchi", "familiya": "", "guruh": "Mars", "coins": 0}
        USERS_DATA[target_id]["coins"] += amount
        current_coins = USERS_DATA[target_id]["coins"]
        await message.answer(f"✅ ID: `{target_id}` bo'lgan foydalanuvchiga **{amount}** coin qo'shildi!\n🪙 Hozirgi balansi: {current_coins} coin.", parse_mode=ParseMode.MARKDOWN)
        await bot.send_message(chat_id=target_id, text=f"🎉 **Xushxabar!**\nAdmin tomonidan hisobingizga **{amount} Mars Coin** qo'shildi!\n🪙 Hozirgi balansingiz: {current_coins} coin.", parse_mode=ParseMode.MARKDOWN)
    except (IndexError, ValueError):
        await message.answer("❌ Xato format. To'g'ri foydalanish:\n`/plus [user_id] [miqdor]`", parse_mode=ParseMode.MARKDOWN)

@dp.callback_query(F.data.startswith("reply_"))
async def admin_reply_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Siz admin emassiz!", show_alert=True)
        return
    target_user_id = int(callback.data.split("_")[1])
    await state.update_data(target_user=target_user_id)
    await callback.message.answer(f"👤 ID: `{target_user_id}` bo'lgan foydalanuvchiga javobingizni kiriting:")
    await state.set_state(BotStates.admin_waiting_reply)
    await callback.answer()

@dp.message(BotStates.admin_waiting_reply)
async def admin_send_reply_to_user(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    data = await state.get_data()
    target_user_id = data.get("target_user")
    try:
        user_msg = f"🔔 **Admindan javob keldi:**\n\n{message.text}"
        await bot.send_message(chat_id=target_user_id, text=user_msg, parse_mode=ParseMode.MARKDOWN)
        await message.answer("✅ Javobingiz foydalanuvchiga muvaffaqiyatli yuborildi!")
    except Exception as e:
        await message.answer(f"❌ Xabar yuborishda xatolik: {e}")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())