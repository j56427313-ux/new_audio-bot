"""
Botning barcha ReplyKeyboardMarkup, KeyboardButton va Inline tugmalari shu yerda.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🤝 Sherik kerak"))
    builder.add(KeyboardButton(text="🏢 Ish joyi kerak"))
    builder.add(KeyboardButton(text="👔 Hodim kerak"))
    builder.add(KeyboardButton(text="👨‍🏫 Ustoz kerak"))
    builder.adjust(2)  # 2x2 formatda
    return builder.as_markup(resize_keyboard=True)


def orqaga_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="⬅️ Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def telefon_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📱 Raqamni yuborish", request_contact=True))
    builder.add(KeyboardButton(text="⬅️ Orqaga"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def admin_tasdiqlash_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="✅ Tasdiqlash",
            callback_data=f"tasdiqlash:{user_id}"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="❌ Rad etish",
            callback_data=f"radetish:{user_id}"
        )
    )
    builder.adjust(2)
    return builder.as_markup()