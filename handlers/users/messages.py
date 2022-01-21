import asyncio
import random
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.menu import main_menu
from aiogram.dispatcher import dispatcher
from aiogram import Dispatcher
from aiogram.dispatcher import filters
from keyboards.inlinebuttons import buttons
from loader import bot
from database.sqlite_database import Connection, DBControl
from Bitcoin_parse import get_currency
from handlers.users.cache import CacheStorage
import os


HOST, PASSWORD, DATABASE, USER = os.getenv("HOST"), os.getenv("PASSWORD"), os.getenv("DATABASE"), os.getenv("USER")
_cache = CacheStorage()
_conn = Connection(host=HOST, password=PASSWORD, database=DATABASE, user=USER).connect()


# wallets
WALLETS = [
    "bc1q9f2vxhnrd4yn22nary7zy555r3fgenhajquhya",
    "bc1q48xeznly02m7xszcx0gpt8wlh3vt5dcqt68klp",
    "bc1qrqsh7m82f5htt8hjjjv8c2v9yhq8t0kqjj7fg7",
    "bc1q7qct55uh68rt07zgxef07kw2cq6mkttj92l9ez",
    "bc1qzvrqwre62r74am5flgsllxd4w3kfsd6kdwfm0a",
    "bc1q94qgmwvfljm5nf5rq5g7dhwq00y05vyw5n7vhe",
    "bc1qhrgz54w6pf395kypthvwz4kzxgnjmnzmet7kux",
    "bc1qlr56c9h9tt73ww5u48se0yxh2wxhpcsyqwxxct",
    "bc1qkgamy20g2rp0aks2h6q6hnt5cdlsf2xcp8zlwk",
    "bc1quz5yntykvkr5n6ll836dnz8m658n9673a5ffnj",
]


async def choice(message: Message):
    if message.text == '🔙 Back to main menu':
        await message.answer(text='Moving back', reply_markup=main_menu.main_menu)
    elif message.text == "🌎 Regions":
        await message.answer(text=message.text, reply_markup=main_menu.region_menu)
    else:
        await message.answer(text=message.text, reply_markup=main_menu.Balance_menu)


async def text_generate(message=None, callback=None, reply_markup=None, text="") -> None:
    if message is not None:
        current = await _cache.get_user(message.from_user.id)
    else:
        current = await _cache.get_user(callback.from_user.id)

    current = (current['data'][current['position']])
    description = f"💰 Card current balance: {current[1]}$\n" \
                  f"🖊 description: {current[2]}\n" \
                  f"🌎 Card region: {current[3]}\n" \
                  f"💵 Price: {current[4]}$\n" \

    if message is not None and callback is None:
        await bot.send_photo(caption=description + text, photo=current[0],
                             chat_id=message.from_user.id, reply_markup=reply_markup)

    elif callback is not None and message is None:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_photo(chat_id=callback.from_user.id, reply_markup=reply_markup,
                             caption=description + text, photo=current[0])


async def first_message(message: Message) -> None:
    parse = await _cache.get_user(message.from_user.id)
    if len(parse["data"]) > 1:
        await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
        await text_generate(message=message, reply_markup=buttons.inline_markup_start)

    elif len(parse["data"]) == 1:
        await message.answer(text=message.text, reply_markup=ReplyKeyboardRemove())
        await text_generate(message=message, reply_markup=buttons.only_one_elem)


async def get_data(message: Message) -> None:
    base = DBControl(connection=_conn)
    if message.text.startswith("💸"):
        data = message.text.split()
        parse = base.balance((data[1], data[3]))
        if parse == []:
            await message.answer(text="Coming soon...", reply_markup=main_menu.back_to_main_menu_only)
        else:
            await _cache.add(key=message.from_user.id, data=parse)
            await first_message(message=message)

    else:
        data = message.text.split()
        parse = base.region((data[1].upper(),))
        if parse == []:
            await message.answer(text="Coming soon...", reply_markup=main_menu.back_to_main_menu_only)
        else:
            await _cache.add(key=message.from_user.id, data=parse)
            await first_message(message=message)


async def call_back_data(callback: CallbackQuery) -> None:
    try:
        current_user = await _cache.get_user(callback.from_user.id)
        position = current_user["position"]

        if callback.data == 'buy_button':
            await text_generate(callback=callback, text='\nAre you sure you want to buy this item?',
                                reply_markup=buttons.inline_markup_yes_no)
            current_user["position"] = 0

        elif callback.data == 'no':
            await text_generate(reply_markup=buttons.only_one_elem, callback=callback)
            current_user["position"] = 0

        elif callback.data == 'yes':
            cash = current_user["data"][current_user["position"]][4]
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(text='Preparing wallet for you...', chat_id=callback.from_user.id)
            btc = await get_currency(int(float(cash.rstrip("$"))))
            wallet = random.choice(WALLETS)
            await bot.send_message(text=f'Now you have 20 minutes to pay {cash}$\n'
                                        f'that equals *{btc}* on this wallet\n*{wallet}*\n'
                                        f'then just click on button check payment',
                                   chat_id=callback.from_user.id, parse_mode='Markdown',
                                   reply_markup=buttons.inline_markup_cancel)
            current_user["position"] = 0

        elif callback.data == 'cancel':
            await asyncio.sleep(random.randint(1, 2))
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(text='turning you back...', reply_markup=main_menu.main_menu,
                                   chat_id=callback.from_user.id)
            current_user["position"] = 0

        elif callback.data == 'check_pm':
            await callback.answer(text="I can't see any transactions", show_alert=True)

        if callback.data == 'Back to main menu':
            try:
                await _cache.delete(callback.from_user.id)
            except Exception as ex:
                print(ex)
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, text=f"🔙 Moving back", reply_markup=main_menu.main_menu)

        if callback.data == 'next_elem':
            if position == len(current_user["data"]) - 2:
                await _cache.increase(callback.from_user.id)
                await text_generate(reply_markup=buttons.inline_markup_final, callback=callback)
            else:
                await _cache.increase(callback.from_user.id)
                await text_generate(reply_markup=buttons.inline_markup_middle, callback=callback)

        elif callback.data == 'prev_elem':
            if position == 1:
                await _cache.decrease(callback.from_user.id)
                await text_generate(reply_markup=buttons.inline_markup_start, callback=callback)
            else:
                await _cache.decrease(callback.from_user.id)
                await text_generate(reply_markup=buttons.inline_markup_middle, callback=callback)

    except Exception as ex:
        print(ex)
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(text="This blank expired, turning you back...", chat_id=callback.from_user.id,
                               reply_markup=main_menu.main_menu)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(choice, dispatcher.Text(equals=['🌎 Regions',
                                                                '💰 Balance',
                                                                '🔙 Back to main menu'], ignore_case=True))

    dp.register_message_handler(get_data, filters.Text(equals=["🇪🇺 EU", "🇺🇸 US", '💸 20$ - 100$', '💸 100$ - 1000$',
                                                               '💸 1000$ - 3500$', '💸 4000$ - 10000$'], ignore_case=True))

    dp.register_callback_query_handler(call_back_data, filters.Text(
        equals=['next_elem', 'prev_elem', 'Back to main menu', 'buy_button', 'yes', 'no', 'cancel', 'check_pm'])
    )
