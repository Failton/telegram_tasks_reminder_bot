from ..utils.create_db import create_db

from .states import UserStates

from aiogram.types import Message
from aiogram import Dispatcher


async def set_offset(message: Message):
    await message.answer('🕑 Write the offset from UTC in minutes (e.g. UTC+03:00 is 180, UTC-05:30 is -330)')
    await UserStates.offset.set()

def register_handlers_set_offset(dp: Dispatcher):
    dp.register_message_handler(set_offset, commands="set_offset", state="*")
