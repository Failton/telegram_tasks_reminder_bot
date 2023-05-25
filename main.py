from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio

from app.utils.create_db import create_db
from app.handlers.help import register_handlers_help
from app.handlers.start import register_handlers_start
from app.handlers.admin import register_handlers_admin
from app.handlers.add_tasks import register_handlers_add_tasks
from app.handlers.tasks import register_handlers_tasks
from app.handlers.my_settings import register_handlers_my_settings
from app.handlers.set_offset import register_handlers_set_offset
from app.inline.button_delete import register_handlers_button_delete

from app.utils.tasks_checker import check_for_tasks
from app.config.config import API_TOKEN



sqlite_connection = create_db()

async def set_default_commands(bot: Bot):
    commands = [
            types.BotCommand("tasks", "💼 Show tasks"),
            # types.BotCommand("admin", "Admin panel"),
            types.BotCommand("set_offset", "🕑 Change UTC offset"),
            types.BotCommand("my_settings", "🔧 Show settings"),
            types.BotCommand("help", "❔ Help"),
            ]
    await bot.set_my_commands(commands)


async def main():
    # LOGGING SETTING
    logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)

    await set_default_commands(bot)
    
    register_handlers_help(dp)
    register_handlers_start(dp)
    register_handlers_admin(dp)
    register_handlers_tasks(dp)
    register_handlers_my_settings(dp)
    register_handlers_set_offset(dp)
    register_handlers_add_tasks(dp)
    register_handlers_button_delete(dp)
    asyncio.ensure_future(check_for_tasks(bot, ))
    
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
