from aiogram import executor
from loader import dp
from logs.logging import on_startup_notify, on_shutdown_notify
from handlers.users import messages, commands
from admin_panel import admin_panel
from database import sqlite_database


async def on_startup_notice(dp):
    await on_startup_notify(dp)
    sqlite_database.database_initialization()


async def on_shutdown_notice(dp):
    await on_shutdown_notify(dp)


commands.register_handler_commands(dp)
messages.register_message_handler(dp)
admin_panel.register_handler_admin(dp)
messages.register_handler_unknown_command(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup_notice, on_shutdown=on_shutdown_notice)
