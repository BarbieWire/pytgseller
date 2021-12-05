from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


all_buttons = []
final_list = []

main_menu = ReplyKeyboardMarkup([
    [
     KeyboardButton(text='🌎 Regions')
    ],
    [
     KeyboardButton(text='💰 Balance')
    ],
], resize_keyboard=True)


# --- Region menu --- #
EU_button = KeyboardButton("🇪🇺 EU")
US_button = KeyboardButton("🇺🇸 US")
region_menu = ReplyKeyboardMarkup(resize_keyboard=True)
region_menu.add(EU_button, US_button)

back_to_main_menu_only = ReplyKeyboardMarkup([
    [
     KeyboardButton(text="🔙 Back to main menu")
    ]
], resize_keyboard=True)


# --- Balance Menu --- #
first_button = KeyboardButton(text='💸 20$ - 100$')
second_button = KeyboardButton(text='💸 100$ - 1000$')
third_button = KeyboardButton(text='💸 1000$ - 3500$')
fourth_button = KeyboardButton(text='💸 4000$ - 10000$')
fifth_button = KeyboardButton(text='🔙 Back to main menu')

Balance_menu = ReplyKeyboardMarkup(resize_keyboard=True)
Balance_menu.add(first_button, second_button, third_button, fourth_button, fifth_button)

for button in dict(region_menu).get("keyboard"):
    for dictionary in button:
        dictionary = dictionary.get('text')
        final_list.append(dictionary)


# --- final treatment --- #
for button in dict(Balance_menu).get("keyboard"):
    for dictionary in button:
        dictionary = dictionary.get('text')
        final_list.append(dictionary)

for expand in all_buttons:
    expand = expand.get('text')
    final_list.append(expand)

filtered = filter(lambda x: x != '🔙 Back to main menu', final_list)
final_list = list(filtered)
