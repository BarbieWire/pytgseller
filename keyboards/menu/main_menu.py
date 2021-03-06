from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- main menu --- #
main_menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='π Regions')],
    [KeyboardButton(text='π° Balance')]], resize_keyboard=True)

back_to_main_menu_only = ReplyKeyboardMarkup(
    [[KeyboardButton(text="π Back to main menu")]], resize_keyboard=True
)

# --- Region menu --- #
region_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton(text="πͺπΊ EU"),
    KeyboardButton(text="πΊπΈ US"),
    KeyboardButton(text="π Back to main menu")
)

# --- Balance Menu --- #
Balance_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='πΈ 20$ - 100$'),
    KeyboardButton(text='πΈ 100$ - 1000$'),
    KeyboardButton(text='πΈ 1000$ - 3500$'),
    KeyboardButton(text='πΈ 4000$ - 10000$'),
    KeyboardButton(text='π Back to main menu')
)
