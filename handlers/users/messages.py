import asyncio
import random
from aiogram.types import Message, CallbackQuery
from keyboards.menu import main_menu
from aiogram.dispatcher import dispatcher
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from keyboards.menu.main_menu import final_list
from keyboards.inlinebuttons import buttons
from loader import bot
from aiogram.types import ReplyKeyboardRemove
from database.sqlite_database import get_data_from_db
from Bitcoin_parse import get_currency

parsed_data = "HERE WILL BE DATA FROM DB"
counter = 0


async def am_reg(message: Message):
    if message.text == '🌎 Regions':
        await message.answer(text=message.text, reply_markup=main_menu.region_menu)

    elif message.text == '💰 Balance':
        await message.answer(text='Moving to Balance', reply_markup=main_menu.Balance_menu)

    elif message.text == '🔙 Back to main menu':
        await message.answer(text='Moving back', reply_markup=main_menu.main_menu)

    elif message.text in main_menu.final_list and message.text != '🔙 Back to main menu':
        await message.answer(message.text)


def parse_data_from_db(message: Message):
    parse_list = get_data_from_db()

    for i in parse_list:
        try:
            global parsed_data
            parsed_data = list(i[message.text])
            return parsed_data

        except Exception as ex:
            print(f'{ex}')


def text_generate():
    try:
        text = f"💰 Card current balance: {parsed_data[counter][1]}\n" \
               f"🖊 description: {parsed_data[counter][2]}\n" \
               f"🌎 Card region: {parsed_data[counter][3]}\n" \
               f"💵 Price: {parsed_data[counter][4]}\n"
        return text
    except Exception as ex:
        print(parsed_data[counter])


async def first_message(message: Message):
    global parsed_data
    global counter

    if len(parsed_data) > 1:
        counter = 0
        text = text_generate()
        await bot.send_photo(caption=text, photo=parsed_data[counter][0],
                             chat_id=message.from_user.id,
                             reply_markup=buttons.inline_markup_start)
    elif len(parsed_data) == 1:
        counter = 0
        text = text_generate()
        await bot.send_photo(caption=text, photo=parsed_data[counter][0],
                             chat_id=message.from_user.id,
                             reply_markup=buttons.only_one_elem)
    else:
        await message.answer(text='Coming soon...', reply_markup=buttons.only_back_to_main_menu)


async def inline_template(message: Message):
    markup = ReplyKeyboardRemove()
    position = message.text

    if message.text == '💸 20$ - 100$':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position}', reply_markup=markup)
        await first_message(message)

    elif message.text == '💸 100$ - 1000$':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position}', reply_markup=markup)
        await first_message(message)

    elif message.text == '💸 1000$ - 3500$':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position}', reply_markup=markup)
        await first_message(message)

    elif message.text == '💸 4000$ - 10000$':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position}', reply_markup=markup)
        await first_message(message)

    elif message.text == '🇪🇺 EU':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position} region 🌎', reply_markup=markup)
        await first_message(message)

    elif message.text == '🇺🇸 US':
        data_parse = parse_data_from_db(message)
        await message.answer(text=F'moving to {position} region 🌎', reply_markup=markup)
        await first_message(message)


async def callbackdata(callback: CallbackQuery):
    global counter
    global parsed_data

    if callback.data == 'buy_button':
        counter = 0
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_photo(chat_id=callback.from_user.id, reply_markup=buttons.inline_markup_yes_no,
                             caption=text_generate() + '\n\nAre you sure you want to buy this item?',
                             photo=parsed_data[counter][0])

    if callback.data == 'no':
        counter = 0
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        text = text_generate()
        await bot.send_photo(chat_id=callback.from_user.id, caption=f"{text}",
                             photo=parsed_data[counter][0], reply_markup=buttons.inline_markup_start)

    if callback.data == 'yes':
        counter = 0
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(text='Preparing wallet for you...', chat_id=callback.from_user.id)
        btc = await get_currency(int(float(parsed_data[counter][4].rstrip("$"))))
        await asyncio.sleep(random.randint(2, 5))
        wallets = open("wallets.txt", "r")
        wallet = random.choice(wallets.readlines())
        await bot.send_message(text=f'Now you have 20 minutes to pay {parsed_data[counter][4]}\n'
                                    f'that equals *{btc}* on this wallet\n*{wallet}*\n'
                                    f'After payment card data will be automatically send by bot',
                               chat_id=callback.from_user.id, parse_mode='Markdown',
                               reply_markup=buttons.inline_markup_cancel)

    if callback.data == 'cancel':
        counter = 0
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await asyncio.sleep(random.randint(1, 3))
        await bot.send_message(chat_id=callback.from_user.id, text='turning you back...',
                               reply_markup=main_menu.main_menu)

    if callback.data == 'Back to main menu':
        counter = 0
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, text=f"🔙 Moving back", reply_markup=main_menu.main_menu)


    if callback.data == 'next_elem':
        if counter == len(parsed_data) - 2:
            counter += 1
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            text = text_generate()
            await bot.send_photo(chat_id=callback.from_user.id, caption=f"{text}",
                                 photo=parsed_data[counter][0], reply_markup=buttons.inline_markup_final)
        else:
            counter += 1
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            text = text_generate()
            await bot.send_photo(chat_id=callback.from_user.id, caption=f"{text}",
                                 photo=parsed_data[counter][0], reply_markup=buttons.inline_markup_middle)

    elif callback.data == 'prev_elem':
        if counter == 1:
            counter -= 1
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            text = text_generate()
            await bot.send_photo(chat_id=callback.from_user.id, caption=f"{text}",
                                 photo=parsed_data[counter][0], reply_markup=buttons.inline_markup_start)
        else:
            counter -= 1
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            text = text_generate()
            await bot.send_photo(chat_id=callback.from_user.id, caption=f"{text}",
                                 photo=parsed_data[counter][0], reply_markup=buttons.inline_markup_middle)


async def unknown(message: Message):
    await message.answer(text='Unknown command!\ntry something else')


async def unknown_photo(message: Message):
    answers = ["I am just a robot, stop send me this", 'Cool photo, man', 'My robot eyes bleeding']
    await message.reply(text=random.choice(answers))


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(am_reg, dispatcher.Text(equals=['🌎 Regions', '💰 Balance', '🔙 Back to main menu'],
                                                        ignore_case=True))
    dp.register_message_handler(inline_template, filters.Text(equals=final_list, ignore_case=True))
    dp.register_callback_query_handler(callbackdata, filters.Text(
        equals=['next_elem', 'prev_elem', 'Back to main menu', 'buy_button', 'yes', 'no', 'cancel']))


def register_handler_unknown_command(dp: Dispatcher):
    dp.register_message_handler(unknown_photo, content_types=['photo'])
    dp.register_message_handler(unknown)
