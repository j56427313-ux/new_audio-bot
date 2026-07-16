from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


menyu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Wikipedia 📝"),
            KeyboardButton(text="Harry Potter 📚"),
            KeyboardButton(text="Valyuta 💰")
        ],
        [
            KeyboardButton(text="Instagram 📷")
        ]
    ],
    resize_keyboard= True
)