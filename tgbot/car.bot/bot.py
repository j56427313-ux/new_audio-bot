import asyncio
from datetime import date
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import logging  
from config import API_TOKEN
from buttons import brendlar, mercedes_buttons,BMW_buttons,Audi_buttons,Tesla_buttons,Porsche_buttons



bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name},Avto salon botimizga xush kelibsiz!",reply_markup=brendlar)

tanlov = ''
@dp.message(F.text == "🚗 Mercedes")
async def mers_heandler(msg:Message):
    await msg.answer("Siz Mercedes brendini tanladingiz,ichidan mashinalar tanlang:",reply_markup=mercedes_buttons)
    global tanlov
    tanlov = msg.text
    

tanlov = ''
@dp.message(F.text == "🚗 BMW")
async def BMW_heandler(msg:Message):
    await msg.answer("Siz BMW brendini tanladingiz,ichidan mashinalar tanlang:",reply_markup=BMW_buttons)
    global tanlov
    tanlov = msg.text
    
    
tanlov = ''
@dp.message(F.text == "🚗 Audi")
async def Audi_heandler(msg:Message):
    await msg.answer("Siz Audi brendini tanladingiz,ichidan mashinalar tanlang:",reply_markup=Audi_buttons)
    global tanlov
    tanlov = msg.text
    
tanlov = ''
@dp.message(F.text == "🚗 Tesla")
async def Tesla_heandler(msg:Message):
    await msg.answer("Siz Tesla brendini tanladingiz,ichidan mashinalar tanlang:",reply_markup=Tesla_buttons)
    global tanlov
    tanlov = msg.text
    
tanlov = ''
@dp.message(F.text == "🚗 Porsche")
async def Porsche_heandler(msg:Message):
    await msg.answer("Siz Porsche brendini tanladingiz,ichidan mashinalar tanlang:",reply_markup=Porsche_buttons)
    global tanlov
    tanlov = msg.text
    
    
@dp.message(F.text)
async def car_handler(msg: Message):
    global tanlov
    try:
        for i in date[tanlov]:
            if msg.text == i["model"]:
                nomi = i["model"]
                yili = i["year"]
                narxi = i["price"]
                rasm = i["image"]
        await msg.answer_photo(photo = rasm, caption =f"{nomi}\nYili:{yili}\nNarxi:{narxi}  $")
    except Exception as e:
        await msg.answer("Iltimos mashina madelini tanlarnfyoki/start ni bosing.")
        logging.error(f"Xatolik yuz berdi:  {e}")
        
        
        
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))