from ..utils.create_db import create_db

from .states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import Dispatcher

sqlite_connection = create_db()

async def start(message: Message):
    cursor = sqlite_connection.cursor()

    cursor.execute('SELECT * FROM users WHERE (user_id=%s)', (message.from_user.id, ))
    user_exists = cursor.fetchone()

    if user_exists is None:
        cursor.execute('INSERT INTO users (user_id, utc_offset, block) VALUES (%s, 0, 0)', (message.from_user.id, ))
        sqlite_connection.commit()

        await message.answer('🕑 Write the offset from UTC in minutes (e.g. UTC+03:00 is 180, UTC-05:30 is -330)')
        await UserStates.offset.set()



async def get_offset(message: Message, state: FSMContext):
    if (message.text.lstrip("-").isdigit() is True and -1440 <= int(message.text) <= 1440):
        cursor = sqlite_connection.cursor()

        cursor.execute('UPDATE users SET utc_offset=%s WHERE user_id=%s', (message.text, message.from_user.id))
        sqlite_connection.commit()

        await message.answer('✅ Done! To create a new task, you can write/forward a message to the bot.')
        await state.finish()
    else:
        await message.answer('❌ Wrong format! Try again')

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(get_offset, state=UserStates.offset)
