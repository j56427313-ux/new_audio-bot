import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter

import logging
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

class Registerstate(StatesGroup):
    ism = State()
    familya = State()
    yosh = State()
    sinf = State()

@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name},\
\nRegister botimizga xush kelibsiz! Royxattan otish uchun /register ni bosing", reply_markup=ReplyKeyboardRemove())


@dp.message(Command("register"))
async def register_handlar(msg:Message, state: FSMContext):
    await msg.answer("Registratsiya boshlandi, ismingizni kiriting:")
    await state.set_state(Registerstate.ism)

@dp.message(StateFilter(Registerstate.ism))
async def ism_handlar(msg:Message, state: FSMContext):
    x = msg.text
    await state.update_data(ism=x)
    await msg.answer("Ism qabul qilindi, familyangizni kiriting:")
    await state.set_state(Registerstate.familya)


@dp.message(StateFilter(Registerstate.familya))
async def fam_handlar(msg:Message, state: FSMContext):
    x = msg.text
    await state.update_data(familya=x)
    await msg.answer("Familya qabul qilindi, yoshingizni kiriting:")
    await state.set_state(Registerstate.yosh)


@dp.message(StateFilter(Registerstate.yosh))
async def yosh_handlar(msg:Message, state: FSMContext):
    x = msg.text
    if not x.isdigit():
        await msg.answer("Iltimos, yoshingizni faqat raqam bilan kiriting!")
        return
    await state.update_data(yosh=x)
    await msg.answer("Yosh qabul qilindi, nechanchi sinfda oqiysiz?:")
    await state.set_state(Registerstate.sinf)


@dp.message(StateFilter(Registerstate.sinf))
async def sinf_handlar(msg:Message, state: FSMContext):
    x = msg.text
    await state.update_data(sinf=x)
    data = await state.get_data()
    await msg.answer(f"Royxattan otish yakunlandi! Sizning ma'lumotlaringiz:\nIsm: {data['ism']}\nFamilya: {data['familya']}\nYosh: {data['yosh']}\nSinf: {data['sinf']}")
    await state.clear()


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))