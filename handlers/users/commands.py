from aiogram.types import Message
from keyboards.menu import main_menu
from loader import bot


# @dp.message_handler(commands=['start'])
async def introduction_command(message: Message):
    user = message.from_user.full_name
    answer = F"Hello, {user}! \nI'm your personal credit card seller. \nHere you can find everything for every taste\n"\
             F"\nNow you can select one of the items below\n" \
             F"/help - for more information"
    await bot.send_photo(caption=answer, photo=open('logo.jpg', 'rb'), reply_markup=main_menu.main_menu,
                         chat_id=message.from_user.id)


# @dp.message_handler(commands=['help'])
async def help_command(message: Message):
    first = "Huh, seems like you need some kind of help with purchasing..."
    second = "First of all you need to back in main" \
             "menu to find position that you are interested in.\nThen you can see list of available products and whole " \
             "info about product if you liked something just click 'buy' button and send equivalent amount on " \
             "wallet below, bot will automatically send all chosen credit card data"

    await bot.send_animation(caption=first, animation=open('help.gif', 'rb'), chat_id=message.from_user.id)
    await message.answer(second, reply_markup=main_menu.main_menu)


def register_handler_commands(dp):
    dp.register_message_handler(introduction_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
