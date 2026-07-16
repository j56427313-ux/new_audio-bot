from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import data

# Bosh sahifa — brendlar
brendlar = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚗 Mercedes", callback_data="brand:🚗 Mercedes"),
        InlineKeyboardButton(text="🚗 BMW",      callback_data="brand:🚗 BMW"),
    ],
    [
        InlineKeyboardButton(text="🚗 Audi",     callback_data="brand:🚗 Audi"),
        InlineKeyboardButton(text="🚗 Tesla",    callback_data="brand:🚗 Tesla"),
    ],
    [
        InlineKeyboardButton(text="🚗 Porsche",  callback_data="brand:🚗 Porsche"),
    ],
])


def get_cars_keyboard(brand: str) -> InlineKeyboardMarkup:
    """Tanlangan brendning 5 ta mashinasi ro'yxati."""
    rows = []
    for idx, car in enumerate(data[brand]):
        rows.append([
            InlineKeyboardButton(text=car["model"], callback_data=f"car:{brand}:{idx}")
        ])
    rows.append([
        InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="home"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_car_nav_keyboard(brand: str, idx: int) -> InlineKeyboardMarkup:
    """Mashina rasmining tagidagi navigatsiya tugmalari."""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔙 Orqaga",      callback_data=f"brand:{brand}"),
        InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="home"),
    ]])