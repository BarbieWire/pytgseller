from aiogram.types import Message
import random
from aiogram import Dispatcher


async def unknown(message: Message):
    await message.answer(text='Unknown command!\ntry something else')


async def unknown_photo(message: Message):
    answers = ["I am just a robot, stop send me this", 'Cool photo, man', 'My robot eyes bleeding']
    await message.reply(text=random.choice(answers))


def register_handler_unknown_command(dp: Dispatcher):
    dp.register_message_handler(unknown_photo, content_types=['photo'])
    dp.register_message_handler(unknown)
