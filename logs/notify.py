from aiogram import Dispatcher
from dotenv import load_dotenv
import os


load_dotenv(".env")
ADMINS = os.getenv("ADMINS")


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS.split():
        await dp.bot.send_message(admin, "Бот Запущен")


async def on_shutdown_notify(dp: Dispatcher):
    for admin in ADMINS.split():
        await dp.bot.send_message(admin, "Бот Выключен")
