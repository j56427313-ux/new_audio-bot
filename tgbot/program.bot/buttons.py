from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data import data

# Asosiy menyu: Backend va Frontend
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚙️ Backend"), KeyboardButton(text="🖥️ Frontend")],
    ],
    resize_keyboard=True,
)


def make_types_keyboard(category: str) -> ReplyKeyboardMarkup:
    """Tanlangan kategoriya uchun 5 ta tur tugmalari."""
    items = data[category]
    keyboard = [[KeyboardButton(text=f"{item['icon']} {item['name']}")] for item in items]
    keyboard.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)