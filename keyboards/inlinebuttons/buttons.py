from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_markup_middle = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Previous', callback_data='prev_elem'),
    InlineKeyboardButton(text='Buy', callback_data='buy_button'),
    InlineKeyboardButton(text='Next', callback_data='next_elem'),
    InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu')
)

inline_markup_start = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Buy', callback_data='buy_button'),
    InlineKeyboardButton(text='Next', callback_data='next_elem'),
    InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu')
)

inline_markup_final = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Previous', callback_data='prev_elem'),
    InlineKeyboardButton(text='Buy', callback_data='buy_button'),
    InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu')
)

only_back_to_main_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu')
)

only_one_elem = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu'),
    InlineKeyboardButton(text='Buy', callback_data='buy_button')
)

inline_markup_yes_no = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Yes', callback_data='yes'),
    InlineKeyboardButton(text='No', callback_data='no')
)

inline_markup_cancel = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Cancel', callback_data='cancel'),
    InlineKeyboardButton(text='Check payment', callback_data='check_pm')
)
