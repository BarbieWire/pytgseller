from aiogram import Dispatcher, Bot
# from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")


storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
