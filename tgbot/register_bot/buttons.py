from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


telefon_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞Telefon raqam yuborish", request_contact=True)]
], resize_keyboard=True)

lokatsiya_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📍Lokatsiya yuborish", request_location=True)]
], resize_keyboard=True)