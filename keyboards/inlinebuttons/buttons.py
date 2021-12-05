from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_markup_middle = InlineKeyboardMarkup()
next_item = InlineKeyboardButton(text='Next', callback_data='next_elem')
previous = InlineKeyboardButton(text='Previous', callback_data='prev_elem')
buy_button = InlineKeyboardButton(text='Buy', callback_data='buy_button')
back_to_main_menu = [InlineKeyboardButton(text='🔙 Back to main menu', callback_data='Back to main menu')]

inline_markup_middle.add(previous, buy_button, next_item)
inline_markup_middle.row(*back_to_main_menu)

inline_markup_start = InlineKeyboardMarkup(row_width=2)
inline_markup_start.add(buy_button, next_item, *back_to_main_menu)

inline_markup_final = InlineKeyboardMarkup(row_width=2)
inline_markup_final.add(previous, buy_button, *back_to_main_menu)

only_back_to_main_menu = InlineKeyboardMarkup(row_width=1)
only_back_to_main_menu.add(*back_to_main_menu)

only_one_elem = InlineKeyboardMarkup()
only_one_elem.add(*back_to_main_menu, buy_button)

inline_markup_yes_no = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(text='Yes', callback_data='yes')
no_button = InlineKeyboardButton(text='No', callback_data='no')
inline_markup_yes_no.add(no_button, *back_to_main_menu, yes_button)

inline_markup_cancel = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Cancel', callback_data='cancel')
)
