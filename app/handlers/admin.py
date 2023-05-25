from aiogram.types import Message
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .states import UserStates
from ..utils.create_db import create_db
from ..config.config import ADMIN_ID

sqlite_connection = create_db()

async def admin(message: Message):
    admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    admin_buttons.add(types.InlineKeyboardButton(text="Рассылка"))
    admin_buttons.add(types.InlineKeyboardButton(text="Статистика"))
    admin_buttons.add(types.InlineKeyboardButton(text="Выйти из админ-панели"))

    if message.from_user.id == ADMIN_ID:
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=admin_buttons)
        await UserStates.admin_actions.set()
    else:
        await message.answer('Вы не имеете доступа к этому разделу.')


async def admin_actions(message: types.Message, state: FSMContext):
    admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if (message.text == 'Рассылка'):
        admin_buttons.add(types.InlineKeyboardButton(text="Отмена"))
        admin_buttons.add(types.InlineKeyboardButton(text="Статистика"))
        admin_buttons.add(types.InlineKeyboardButton(text="Выйти из админ-панели"))
        await message.answer('Введите сообщение для рассылки', reply_markup=admin_buttons)
        await UserStates.spam.set()
    elif (message.text == 'Статистика'):
        admin_buttons.add(types.InlineKeyboardButton(text="Рассылка"))
        admin_buttons.add(types.InlineKeyboardButton(text="Статистика"))
        admin_buttons.add(types.InlineKeyboardButton(text="Выйти из админ-панели"))

        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT COUNT(user_id) FROM users')
        num_of_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(task_id) FROM tasks')
        num_of_tasks = cursor.fetchone()[0]
        await message.answer(f'Число юзеров, запустивших бота: {num_of_users}\n\nКоличество всех задач: {num_of_tasks}', reply_markup=admin_buttons)
        await UserStates.admin_actions.set()
    elif (message.text == 'Выйти из админ-панели'):
        await message.answer('Вышел...', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        admin_buttons.add(types.InlineKeyboardButton(text="Рассылка"))
        admin_buttons.add(types.InlineKeyboardButton(text="Статистика"))
        admin_buttons.add(types.InlineKeyboardButton(text="Выйти из админ-панели"))
        await message.answer('Неизвестная команда', reply_markup=admin_buttons)


async def start_spam(message: Message, state: FSMContext):
    admin_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    admin_buttons.add(types.InlineKeyboardButton(text="Рассылка"))
    admin_buttons.add(types.InlineKeyboardButton(text="Статистика"))
    admin_buttons.add(types.InlineKeyboardButton(text="Выйти из админ-панели"))

    if message.text == 'Отмена':
        await message.answer('Отменено', reply_markup=admin_buttons)
        await UserStates.admin_actions.set()
    elif message.text == 'Выйти из админ-панели':
        await message.answer('Вышел...', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    else:
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT user_id FROM users')
        spam_base = cursor.fetchall()

        for i in range(len(spam_base)):
            await bot.send_message(spam_base[i][0], message.text)

        await message.answer('Рассылка завершена', reply_markup=admin_buttons)
        await UserStates.admin_actions.set()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin", state="*")
    dp.register_message_handler(admin_actions, state=UserStates.admin_actions)
    dp.register_message_handler(start_spam, state=UserStates.spam)
