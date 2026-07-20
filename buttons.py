from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Faqat "⬅️ Orqaga" tugmasi bo'lgan sodda menyu (masalan, Wikipedia bo'limi uchun)
orqaga_menyu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Orqaga")]
    ],
    resize_keyboard=True
)


menyu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Wikipedia 📝"),
            KeyboardButton(text="Harry Potter 📚"),
            KeyboardButton(text="Valyuta 💰")
        ],
        [
            KeyboardButton(text="Instagram 📷"),
            KeyboardButton(text="Ovoz 🎙️"),
            KeyboardButton(text="Rasm 🖼️")
        ]
    ],
    resize_keyboard=True
)


# ====================== 🎙️ OVOZ BO'LIMI ======================

ovoz_menyu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗣 Matn → Ovoz"),
            KeyboardButton(text="🎧 Ovoz → Matn")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga")
        ]
    ],
    resize_keyboard=True
)


# ====================== 🖼️ RASM BO'LIMI ======================

rasm_menyu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚫ Oq-qora"),
            KeyboardButton(text="🌫 Blur")
        ],
        [
            KeyboardButton(text="✏️ Cartoon/Anime effekt"),
            KeyboardButton(text="🧼 Fon olib tashlash")
        ],
        [
            KeyboardButton(text="🎭 Yuz mesh filtri"),
            KeyboardButton(text="🔤 Matnni o'qish (OCR)")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga")
        ]
    ],
    resize_keyboard=True
)

# Tugma matni -> image_utils.py dagi filtr nomi
RASM_FILTRLARI = {
    "⚫ Oq-qora": "grayscale",
    "🌫 Blur": "blur",
    "✏️ Cartoon/Anime effekt": "cartoon",
    "🧼 Fon olib tashlash": "remove_bg",
    "🎭 Yuz mesh filtri": "face_mesh",
    "🔤 Matnni o'qish (OCR)": "ocr",
}