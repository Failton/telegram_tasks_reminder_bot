from aiogram.types import Message
from aiogram import Dispatcher

async def help(message: Message):
    await message.answer('🔹 To create a new task, you can write/forward a message to the bot, then select a date and time.\n\n🔸 When the time comes, the bot will remind you of your task.\n\n💻 @failton - for feedback')


def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(help, commands="help", state="*")
