from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# ================= REPLY BUTTON =================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Fanlar"),
            KeyboardButton(text="👨‍🏫 O'qituvchilar")
        ],
        [
            KeyboardButton(text="📅 Dars Jadvali"),
            KeyboardButton(text="☎️ Aloqa")
        ]
    ],
    resize_keyboard=True
)



# ================= FANLAR INLINE =================

fan_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Matematika",
                callback_data="matematika"
            )
        ],
        [
            InlineKeyboardButton(
                text="💻 Informatika",
                callback_data="informatika"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚗️ Kimyo",
                callback_data="kimyo"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌍 Geografiya",
                callback_data="geografiya"
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 Ona tili",
                callback_data="ona_tili"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇬🇧 Ingliz tili",
                callback_data="ingliz"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚛️ Fizika",
                callback_data="fizika"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌱 Biologiya",
                callback_data="biologiya"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎨 San'at",
                callback_data="sanat"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏃 Sport",
                callback_data="sport"
            )
        ]
    ]
)



# ================= O'QITUVCHILAR =================

teacher_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Matematika o'qituvchisi",
                callback_data="oq1"
            )
        ],
        [
            InlineKeyboardButton(
                text="💻 Informatika o'qituvchisi",
                callback_data="oq2"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚗️ Kimyo o'qituvchisi",
                callback_data="oq3"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌍 Geografiya o'qituvchisi",
                callback_data="oq4"
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 Ona tili o'qituvchisi",
                callback_data="oq5"
            )
        ]
    ]
)



# ================= DARS JADVALI =================

days_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Dushanba",
                callback_data="du"
            )
        ],
        [
            InlineKeyboardButton(
                text="Seshanba",
                callback_data="se"
            )
        ],
        [
            InlineKeyboardButton(
                text="Chorshanba",
                callback_data="chor"
            )
        ],
        [
            InlineKeyboardButton(
                text="Payshanba",
                callback_data="pay"
            )
        ],
        [
            InlineKeyboardButton(
                text="Juma",
                callback_data="ju"
            )
        ]
    ]
)