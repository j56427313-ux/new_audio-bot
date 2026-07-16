from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# --- Bosh menyu (5 ta tugma) ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Profil"), KeyboardButton(text="🪙 Coin")],
        [KeyboardButton(text="🚀 Space shop"), KeyboardButton(text="🏫 Maktab haqida")],
        [KeyboardButton(text="✍️ Izoh qoldirish")]
    ],
    resize_keyboard=True
)

# --- Space Shop mahsulotlari (10 ta mahsulot) ---
def get_shop_keyboard():
    builder = ReplyKeyboardBuilder()
    products = [
        "🎒 Mars Ryukzak", "👕 Mars Huddi", "🧢 Mars Kepka", "📔 Mars Bloknot", "🥤 Mars Termos",
        "🖱️ Mars Kovrik", "🎧 Mars Naushnik", "🔌 Powerbank", "⌨️ Klaviatura", "🖊️ Mars Ruchka"
    ]
    for product in products:
        builder.add(KeyboardButton(text=product))
    builder.adjust(2)  # Mahsulotlarni 2 qatordan chiqaradi
    # Bosh menyuga qaytish tugmasi
    builder.row(KeyboardButton(text="⬅️ Bosh menyuga qaytish"))
    return builder.as_markup(resize_keyboard=True)

# --- Admin javob berishi uchun inline tugma ---
def get_admin_reply_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="✍️ Javob yozish", 
        callback_data=f"reply_{user_id}"
    ))
    return builder.as_markup()

# --- Izoh yuborishni yakunlash uchun tugma ---
cancel_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True
)