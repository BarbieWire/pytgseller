from aiogram import Dispatcher, Bot
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
