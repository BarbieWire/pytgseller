from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- main menu --- #
main_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='🌎 Regions')],
    [KeyboardButton(text='💰 Balance')]], resize_keyboard=True)

back_to_main_menu_only = ReplyKeyboardMarkup(
    [[KeyboardButton(text="🔙 Back to main menu")]], resize_keyboard=True
)

# --- Region menu --- #
region_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton(text="🇪🇺 EU"),
    KeyboardButton(text="🇺🇸 US"),
    KeyboardButton(text="🔙 Back to main menu")
)

# --- Balance Menu --- #
Balance_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='💸 20$ - 100$'),
    KeyboardButton(text='💸 100$ - 1000$'),
    KeyboardButton(text='💸 1000$ - 3500$'),
    KeyboardButton(text='💸 4000$ - 10000$'),
    KeyboardButton(text='🔙 Back to main menu')
)
