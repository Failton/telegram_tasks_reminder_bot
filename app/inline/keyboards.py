from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tasks_button_delete = InlineKeyboardButton('❌ Delete', callback_data='button_delete')
tasks_buttons = InlineKeyboardMarkup(row_width=1).add(tasks_button_delete)
