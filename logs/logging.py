import logging
from aiogram import Dispatcher
from config import admins


async def on_startup_notify(dp: Dispatcher):
        for admin in admins.split():
            try:
                await dp.bot.send_message(admin, "Бот Запущен")

            except Exception as err:
                logging.exception(err)


async def on_shutdown_notify(dp: Dispatcher):
    for admin in admins.split():
        try:
            await dp.bot.send_message(admin, "Бот Выключен")

        except Exception as err:
            logging.exception(err)
