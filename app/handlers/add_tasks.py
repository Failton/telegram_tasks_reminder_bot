from ..utils.create_db import create_db

from aiogram.dispatcher.filters import MediaGroupFilter

from aiogram_media_group import media_group_handler

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types

from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram_timepicker.panel import FullTimePicker, full_timep_callback

connection = create_db()

@media_group_handler
async def add_task_album(messages: list[Message]):
    cursor = connection.cursor()

    media_group_id = messages[0]['media_group_id']
    message_ids = ''
    caption = ''

    for message in messages:
        if ('caption' in message):
            caption += message['caption']
        if ('photo' in message):
            message_ids += f'photo:{message["photo"][-1]["file_id"]}|'
        elif ('video' in message):
            message_ids += f'video:{message["video"]["file_id"]}|'
        elif ('document' in message):
            message_ids += f'document:{message["document"]["file_id"]}|'

    message_ids = message_ids[:-1]

    chat_id = message.from_user.id
    message_id = message.message_id

    cursor.execute('SELECT utc_offset FROM users WHERE user_id=%s', (chat_id, ))
    offset = cursor.fetchone()[0]

    cursor.execute("INSERT INTO tasks(user_id, utc_offset, date, time, message_id, message_id_to_edit, media_group_id, media_ids, caption) VALUES (%s, %s, ' ', ' ', %s, 0, %s, %s, %s)", (chat_id, offset, message_id, media_group_id, message_ids, caption))
    connection.commit()
    await message.answer('Please select a date:', reply_markup=await SimpleCalendar().start_calendar())


async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    cursor = connection.cursor()

    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)

    if selected:
        await callback_query.message.answer(f'📅 You selected: {date.strftime("%d/%m/%Y")}')
        await callback_query.bot.delete_message(chat_id=chat_id, message_id=(message_id))

    cursor.execute('UPDATE tasks SET date=%s WHERE user_id=%s AND  message_id=%s', (date.strftime("%d/%m/%Y"), chat_id, message_id - 1))
    connection.commit()
    await callback_query.message.answer("Please select a time:", reply_markup=await FullTimePicker().start_picker())


async def process_full_timepicker(callback_query: types.CallbackQuery, callback_data: dict):
    cursor = connection.cursor()

    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    r = await FullTimePicker().process_selection(callback_query, callback_data)

    if r.status.name == 'SELECTED':
        cursor.execute('UPDATE tasks SET time=%s WHERE user_id=%s AND message_id=%s', (r.time.strftime("%H:%M:%S"), chat_id, message_id - 3))
        await callback_query.message.answer(f'🕑 You selected: {r.time.strftime("%H:%M:%S")}')
        await callback_query.message.delete_reply_markup()
        await callback_query.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await callback_query.message.answer('✅ Done!')
    elif r.status.name == 'CANCELED':
        await callback_query.message.answer('❌ Canceled!')
        await callback_query.bot.delete_message(chat_id=chat_id, message_id=message_id - 1)
        cursor.execute('DELETE FROM tasks WHERE user_id=%s AND message_id=%s', (chat_id, message_id - 3))
        connection.commit()


async def add_task(message: Message):
    cursor = connection.cursor()
    chat_id = message.from_user.id
    message_id = message.message_id

    cursor.execute('SELECT utc_offset FROM users WHERE user_id=%s', (chat_id, ))
    offset = cursor.fetchone()[0]

    cursor.execute("INSERT INTO tasks(user_id, utc_offset, date, time, message_id, message_id_to_edit, media_group_id, media_ids, caption) VALUES (%s, %s, ' ', ' ', %s, 0, ' ', ' ', ' ')", (chat_id, offset, message_id))
    connection.commit()

    await message.answer('Please select a date:', reply_markup=await SimpleCalendar().start_calendar())

def register_handlers_add_tasks(dp: Dispatcher):
    dp.register_message_handler(add_task_album, MediaGroupFilter(is_media_group=True), content_types=types.ContentType.ANY)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter())
    dp.register_callback_query_handler(process_full_timepicker, full_timep_callback.filter())
    dp.register_message_handler(add_task, MediaGroupFilter(is_media_group=False), content_types=types.ContentTypes.ANY)
