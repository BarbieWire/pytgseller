from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Dispatcher
import database.sqlite_database
from config import admins
from aiogram.dispatcher.filters import Text
from database.sqlite_database import add_command, readall
from loader import bot


class FSMAdmin(StatesGroup):
    photo = State()
    balance = State()
    description = State()
    region = State()
    price = State()


# @dp.message_handler(commands=['Upload'])
async def start(message: types.Message):
    if str(message.from_user.id) in admins:
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото")


async def cancel(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in admins:
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
            data['balance'] = str(float(message.text)) + '$'
        except:
            data['balance'] = message.text + '$'

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
        data['region'] = message.text

    await FSMAdmin.next()
    await message.reply('Пришли цену карты\nФормат: "10.50" или "150"')


# @dp.message_handler(state=FSMAdmin.price)
async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['price'] = str(float(message.text)) + '$'

        except:
            data['price'] = message.text + '$'

    await add_command(state)
    await state.finish()


async def delete_item(message: types.Message):
    if str(message.from_user.id) in admins:
        data = await readall()
        for i in data:
            await bot.send_photo(photo=i[0], caption=F'{i}', chat_id=message.from_user.id,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Delete', callback_data=f'del {i[2]}')
                                 ))


async def delete_callback(callback: types.CallbackQuery):
    await database.sqlite_database.delete_data_from_db(callback.data.replace('del ', ''))
    await callback.answer(text='Удалено успешно!', show_alert=True)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=['Upload'], state=None)
    dp.register_message_handler(cancel, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(balance_amount, state=FSMAdmin.balance)
    dp.register_message_handler(set_description, state=FSMAdmin.description)
    dp.register_message_handler(set_region, state=FSMAdmin.region)
    dp.register_message_handler(set_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item, commands=["delete"])
    dp.register_callback_query_handler(delete_callback, lambda x: x.data and x.data.startswith('del'))
