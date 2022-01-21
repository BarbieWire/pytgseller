from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Dispatcher
from database.sqlite_database import Connection, DBControl
from aiogram.dispatcher.filters import Text
from loader import bot
from keyboards.menu.main_menu import back_to_main_menu_only
import os


HOST, PASSWORD, DATABASE, USER = os.getenv("HOST"), os.getenv("PASSWORD"), os.getenv("DATABASE"), os.getenv("USER")
ADMINS = [os.getenv("ADMINS")]


class FSMAdmin(StatesGroup):
    photo = State()
    balance = State()
    description = State()
    region = State()
    price = State()


# @dp.message_handler(commands=['Upload'])
async def start(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото", reply_markup=types.ReplyKeyboardRemove())


async def cancel(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await state.finish()
        await message.reply('Отмена сработала')


# @dp.message_handler(content_types=["photo"], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await FSMAdmin.next()
    await message.reply('Пришли балланс карты\nФормат: "10.50" или "150"')


# @dp.message_handler(state=FSMAdmin.balance)
async def balance_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['balance'] = str(float(message.text))
        except Exception as _ex:
            data['balance'] = message.text

    await FSMAdmin.next()
    await message.reply('Пришли описание продукта')


# @dp.message_handler(state=FSMAdmin.description)
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await FSMAdmin.next()
    await message.reply('Пришлите регион карты')


async def set_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text.upper()

    await FSMAdmin.next()
    await message.reply('Пришли цену карты\nФормат: "10.50" или "150"')


# @dp.message_handler(state=FSMAdmin.price)
async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['price'] = str(float(message.text))
        except Exception:
            data['price'] = message.text

    conn = Connection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
    DBControl(connection=conn).add(tuple(data.values()))
    await message.answer(text="Все прошло успешно", reply_markup=back_to_main_menu_only)
    await state.finish()


async def delete_item(message: types.Message):
    conn = Connection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
    data = DBControl(connection=conn).readall()

    if str(message.from_user.id) in ADMINS:
        for i in data:
            await bot.send_photo(photo=i[0], caption=F'{i}', chat_id=message.from_user.id,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Delete', callback_data=f'del {i[2]}'))
                                 )


async def delete_callback(callback: types.CallbackQuery):
    conn = Connection(host=HOST, database=DATABASE, user=USER, password=PASSWORD).connect()
    DBControl(connection=conn).delete(callback.data.replace('del ', ''))
    await callback.answer(text='Удалено успешно!', show_alert=True)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=['Upload'], state=None)
    dp.register_message_handler(cancel, Text(equals="Отмена", ignore_case=True), state=[FSMAdmin.photo,
                                                                                        FSMAdmin.balance,
                                                                                        FSMAdmin.region,
                                                                                        FSMAdmin.price,
                                                                                        FSMAdmin.description,
                                                                                        ])
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(balance_amount, state=FSMAdmin.balance)
    dp.register_message_handler(set_description, state=FSMAdmin.description)
    dp.register_message_handler(set_region, state=FSMAdmin.region)
    dp.register_message_handler(set_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item, commands=["delete"])
    dp.register_callback_query_handler(delete_callback, lambda x: x.data and x.data.startswith('del'))
