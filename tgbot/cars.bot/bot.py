import asyncio
from aiogram import Bot, Dispatcher,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import logging
from config import API_TOKEN
from data import data
from buttons import brendlar, get_cars_keyboard, get_car_nav_keyboard

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(
        f"Assalomu aleykum <b>{msg.from_user.full_name}</b>, Avto salon botimizga xush kelibsiz!\n"
        "Kerakli brendni tanlang:",
        reply_markup=brendlar,
        parse_mode="HTML"
    )


@dp.callback_query()
async def inline_handler(call: CallbackQuery):
    button = call.data

    # ── Brend tanlandi → mashinalar ro'yxati ───────────────
    if button.startswith("brand:"):
        brand = button.split("brand:")[1]
        await call.message.answer(
            f"Siz <b>{brand}</b> brendini tanladingiz.\nMashina modelini tanlang:",
            reply_markup=get_cars_keyboard(brand),
            parse_mode="HTML"
        )

    # ── Mashina tanlandi → rasm + ma'lumot ─────────────────
    elif button.startswith("car:"):
        _, brand, idx_str = button.split(":", 2)
        idx = int(idx_str)
        car = data[brand][idx]

        await call.message.answer_photo(
            photo=car["image"],
            caption=(
                f"🚘 <b>{car['model']}</b>\n"
                f"📅 Yili:  {car['year']}\n"
                f"💵 Narxi: {car['price']}"
            ),
            parse_mode="HTML",
            reply_markup=get_car_nav_keyboard(brand, idx)
        )

    # ── Bosh sahifa ─────────────────────────────────────────
    elif button == "home":
        await call.message.answer(
            "Kerakli brendni tanlang:",
            reply_markup=brendlar
        )

    await call.answer()


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))