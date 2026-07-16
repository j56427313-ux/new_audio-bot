import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import logging  # log larni chiqaradi


bot = Bot(token="token")
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# asinxron va sinxron farqi nima?
# await - return rolida, msg.answer - print

@dp.message(CommandStart())
async def salom_ber(msg: Message):
    await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}, botimizga xush kelibsiz!")
    
@dp.message(Command("youtube"))
async def youtube(msg: Message):
    await msg.reply("YouTube commandasi: .....")
    

@dp.message(Command("instagram"))
async def instagram(msg: Message):
    await msg.reply("Instagram commandasi: .....")
    
@dp.message(F.text)
async def text(msg: Message):
    await msg.reply(f"Siz yozgan text: \n{msg.text}")

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))

# asinxron va sinxron farqi nima?
# bot, dispatcher nima?
# token nima?
# filter nima? Command(), CommandStart()
# message va msg.answer()
# __name__ == '__main__', asyncio.run(dp.start_polling(bot))