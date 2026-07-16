from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

menyu = ReplyKeyboardMarkup(  # 🌐 Tarjima qilish
    keyboard=[
        [
            KeyboardButton(text="🌐 Tarjima qilish"),
        ]
    ],
    resize_keyboard=True,
)

tillar_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
        ],
        [
            InlineKeyboardButton(text="🇫🇷 Français", callback_data="fr"),
            InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"),
            InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="hi"),
        ],
        [
            InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="it"),
            InlineKeyboardButton(text="🇯🇵 日本語", callback_data="ja"),
            InlineKeyboardButton(text="🇰🇷 한국어", callback_data="ko"),
        ],
        [
            InlineKeyboardButton(text="🇵🇹 Português", callback_data="pt"),
            InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"),
            InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data="tr"),
        ],
    ]
)