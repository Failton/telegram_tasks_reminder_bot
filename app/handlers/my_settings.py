from ..utils.create_db import create_db

from aiogram.types import Message
from aiogram import Dispatcher

connection = create_db()

async def my_settings(message: Message):
    cursor = connection.cursor()

    cursor.execute('SELECT utc_offset FROM users WHERE user_id=%s', (message.from_user.id, ))
    settings = cursor.fetchone()

    await message.answer(f'Settings:\n\n🕑 UTC offset: {settings[0]} min.')

def register_handlers_my_settings(dp: Dispatcher):
    dp.register_message_handler(my_settings, commands="my_settings", state="*")
