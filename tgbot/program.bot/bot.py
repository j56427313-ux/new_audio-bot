import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import API_TOKEN
from buttons import main_menu, make_types_keyboard
from data import data

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Har bir foydalanuvchi tanlagan kategoriya: {user_id: "⚙️ Backend"}
user_category: dict[int, str] = {}

# Barcha texnologiya nomlari -> (kategoriya, index) xaritasi
name_to_item: dict[str, tuple[str, int]] = {}
for cat_key, items in data.items():
    for i, item in enumerate(items):
        btn_text = f"{item['icon']} {item['name']}"
        name_to_item[btn_text] = (cat_key, i)


@dp.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(
        f"Assalomu alaykum, <b>{msg.from_user.full_name}</b>! 👋\n\n"
        "Dasturlash yo'nalishini tanlang:",
        
        reply_markup=main_menu,
    )


@dp.message(F.text == "🔙 Orqaga")
async def back_handler(msg: Message):
    user_category.pop(msg.from_user.id, None)
    await msg.answer("Asosiy menyu:", reply_markup=main_menu)


@dp.message(F.text.in_(data.keys()))
async def category_handler(msg: Message):
    cat = msg.text
    user_category[msg.from_user.id] = cat
    cat_name = cat.replace("⚙️ ", "").replace("🖥️ ", "")
    await msg.answer(
        f"<b>{cat_name}</b> bo'limini tanladingiz.\n"
        "Quyidagi texnologiyalardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=make_types_keyboard(cat),
    )


@dp.message(F.text.in_(name_to_item.keys()))
async def tech_handler(msg: Message):
    cat_key, idx = name_to_item[msg.text]
    item = data[cat_key][idx]

    tags_line = " · ".join(f"#{t.replace(' ', '_').replace('/', '_').replace('.', '')}" for t in item["tags"])

    text = (
        f"{item['icon']} <b>{item['name']}</b>\n"
        f"<i>{item['sub']}</i>\n\n"
        f"📌 <b>Tavsif:</b>\n{item['desc']}\n\n"
        f"🏷 <b>Texnologiyalar:</b>\n{tags_line}\n\n"
        f"🚀 <b>Qo'llanilishi:</b>\n{item['uses']}"
    )
    await msg.answer(text, parse_mode="HTML")


@dp.message()
async def unknown_handler(msg: Message):
    await msg.answer(
        "Iltimos, tugmalardan foydalaning yoki /start ni bosing.",
        reply_markup=main_menu,
    )


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))  