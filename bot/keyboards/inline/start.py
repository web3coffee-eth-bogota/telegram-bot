from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("Let's go 🚀", callback_data='step_1'))

    return markup

def get_explanation_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("Understood, next!", callback_data='step_2'))

    return markup

def get_expectations_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("100% work", callback_data='100-0'))
    markup.add(InlineKeyboardButton("70% work and 30% fun", callback_data='70-30'))
    markup.add(InlineKeyboardButton("50% work and 50% fun", callback_data='50-50'))
    markup.add(InlineKeyboardButton("30% work and 70% fun", callback_data='30-70'))
    markup.add(InlineKeyboardButton("100% fun", callback_data='0-100'))

    return markup

def get_location_inline_markup():
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("online", callback_data='online'))
    markup.add(InlineKeyboardButton("offline", callback_data='offline'))

    return markup