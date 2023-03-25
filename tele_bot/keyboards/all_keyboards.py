from aiogram import types 
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu(list_button, column=2):
    buttons = [types.InlineKeyboardButton(text=x, callback_data=x) for x in list_button]
    builder = InlineKeyboardBuilder([buttons])
    builder.adjust(column)
    return builder 



