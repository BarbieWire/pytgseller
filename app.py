from aiogram import executor
from loader import dp
from handlers.users import messages, commands, unknown
from admin_panel import admin_panel
from logs.notify import on_startup_notify, on_shutdown_notify


commands.register_handler_commands(dp)
messages.register_message_handler(dp)
admin_panel.register_handler_admin(dp)
unknown.register_handler_unknown_command(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup_notify, on_shutdown=on_shutdown_notify)
