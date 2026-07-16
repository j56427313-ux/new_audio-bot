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
from buttons import telefon_button, lokatsiya_button

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

class Registerstate(StatesGroup):
    ism = State()
    familya = State()
    yosh = State()
    telefon_raqam = State()
    manzil = State()

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
    await msg.answer("Yosh qabul qilindi, Telefon raqam kiriting:", reply_markup=telefon_button)
    await state.set_state(Registerstate.telefon_raqam)


@dp.message(StateFilter(Registerstate.telefon_raqam))
async def tel_handlar(msg:Message, state: FSMContext):
    if msg.contact is not None:
        x = msg.contact.phone_number
        await state.update_data(telefon_raqam=x)
        await msg.answer("Telefon raqam qabul qilindi, manzilingizni lokatsiya korinishida yuboring:", reply_markup=lokatsiya_button)
        await state.set_state(Registerstate.manzil)
    else:
        await msg.answer("Iltimos, telefon raqam yuboring!")


@dp.message(StateFilter(Registerstate.manzil))
async def manzil_handlar(msg:Message, state: FSMContext):
    if msg.location is not None:
        lat = msg.location.latitude
        lon = msg.location.longitude
        await state.update_data(manzil=f"{lat}, {lon}")
        data = await state.get_data()
        await msg.answer(f"Royxattan otish yakunlandi! Sizning ma'lumotlaringiz:\nIsm: {data['ism']}\nFamilya: {data['familya']}\nYosh: {data['yosh']}\nTelefon raqam: {data['telefon_raqam']}\nManzil: {data['manzil']}", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await msg.answer("Iltimos, lokatsiyani tugma orqali yuboring!")


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))