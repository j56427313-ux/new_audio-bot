import logging
from config import API_TOKEN
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from data import fanlar, teachers, schedule, contact

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = API_TOKEN

# ================= ASOSIY REPLY KEYBOARD =================
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["📚 Fanlar", "👨‍🏫 O'qituvchilar"],
        ["📅 Dars Jadvali", "📞 Aloqa"],
    ],
    resize_keyboard=True,
)

# ================= /start =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Xush kelibsiz!\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=MAIN_KEYBOARD,
    )

def get_fanlar_inline():
    buttons = []
    row = []
    for key, val in fanlar.items():
        row.append(InlineKeyboardButton(val["name"], callback_data=f"fan_{key}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)

# ================= O'QITUVCHILAR INLINE =================
def get_teachers_inline():
    buttons = []
    for key in teachers:
        buttons.append([InlineKeyboardButton(
            teachers[key].split("\n")[0], callback_data=f"teacher_{key}"
        )])
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)

# ================= JADVAL INLINE =================
def get_schedule_inline():
    days = {
        "du": "📅 Dushanba",
        "se": "📅 Seshanba",
        "chor": "📅 Chorshanba",
        "pay": "📅 Payshanba",
        "ju": "📅 Juma",
    }
    buttons = []
    row = []
    for key, name in days.items():
        row.append(InlineKeyboardButton(name, callback_data=f"day_{key}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    return InlineKeyboardMarkup(buttons)

# ================= XABAR HANDLER =================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Fanlar":
        await update.message.reply_text(
            "📚 Fanlardan birini tanlang:",
            reply_markup=get_fanlar_inline(),
        )

    elif text == "👨‍🏫 O'qituvchilar":
        await update.message.reply_text(
            "👨‍🏫 O'qituvchilardan birini tanlang:",
            reply_markup=get_teachers_inline(),
        )

    elif text == "📅 Dars Jadvali":
        await update.message.reply_text(
            "📅 Kunni tanlang:",
            reply_markup=get_schedule_inline(),
        )

    elif text == "📞 Aloqa":
        await update.message.reply_text(
            contact,
            reply_markup=MAIN_KEYBOARD,
        )

    else:
        await update.message.reply_text(
            "❓ Iltimos, quyidagi tugmalardan foydalaning:",
            reply_markup=MAIN_KEYBOARD,
        )

# ================= CALLBACK HANDLER =================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- Fan ma'lumoti ---
    if data.startswith("fan_"):
        key = data.replace("fan_", "")
        fan = fanlar.get(key)
        if fan:
            back_btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Fanlar ro'yxati", callback_data="back_fanlar")]
            ])
            await query.message.reply_photo(
                photo=fan["photo"],
                caption=f"<b>{fan['name']}</b>\n\n{fan['text']}",
                parse_mode="HTML",
                reply_markup=back_btn,
            )

    # --- O'qituvchi ma'lumoti ---
    elif data.startswith("teacher_"):
        key = data.replace("teacher_", "")
        teacher_info = teachers.get(key)
        if teacher_info:
            back_btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 O'qituvchilar", callback_data="back_teachers")]
            ])
            await query.message.reply_text(
                teacher_info,
                reply_markup=back_btn,
            )

    # --- Jadval kunlari ---
    elif data.startswith("day_"):
        key = data.replace("day_", "")
        day_info = schedule.get(key)
        if day_info:
            back_btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Kunlar", callback_data="back_schedule")]
            ])
            await query.message.reply_text(
                day_info,
                reply_markup=back_btn,
            )

    # --- Orqaga tugmalar ---
    elif data == "back_fanlar":
        await query.message.reply_text(
            "📚 Fanlardan birini tanlang:",
            reply_markup=get_fanlar_inline(),
        )

    elif data == "back_teachers":
        await query.message.reply_text(
            "👨‍🏫 O'qituvchilardan birini tanlang:",
            reply_markup=get_teachers_inline(),
        )

    elif data == "back_schedule":
        await query.message.reply_text(
            "📅 Kunni tanlang:",
            reply_markup=get_schedule_inline(),
        )

    elif data == "back_main":
        await query.message.reply_text(
            "🏠 Asosiy menyu:",
            reply_markup=MAIN_KEYBOARD,
        )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()