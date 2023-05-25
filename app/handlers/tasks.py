from ..utils.create_db import create_db

from ..inline.keyboards import tasks_buttons

from aiogram.types import Message
from aiogram import Dispatcher, types


sqlite_connection = create_db()


async def tasks(message: Message):
    cursor = sqlite_connection.cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id=%s', (message.from_user.id, ))
    all_tasks = cursor.fetchall()

    for task in all_tasks:
        chat_id = task[1]
        forward_date = task[3]
        forward_time = task[4]
        message_id = task[5]
        media_group_id = task[7]
        media_ids = task[8].split('|')
        caption = task[9]

        if (media_group_id == ' '):
            message = await message.bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
            message = await message.answer(f'📅 Date: {forward_date}\n⏰ Time: {forward_time}', reply_markup=tasks_buttons)

            cursor.execute('UPDATE tasks SET message_id_to_edit=%s WHERE user_id=%s AND message_id=%s', (message.message_id - 1, chat_id, message_id))
            sqlite_connection.commit()
        else:
            media_group = []

            for i, media in enumerate(media_ids):
                media_type, media_id = media.split(':')

                if (i == 0 and caption != ''):
                    if (media_type == 'photo'):
                        media_group.append(types.InputMediaPhoto(media=media_id, caption=caption))
                    elif (media_type == 'video'):
                        media_group.append(types.InputMediaVideo(media=media_id, caption=caption))
                    elif (media_type == 'document'):
                        media_group.append(types.InputMediaDocument(media=media_id, caption=caption))
                else:
                    if (media_type == 'photo'):
                        media_group.append(types.InputMediaPhoto(media=media_id))
                    elif (media_type == 'video'):
                        media_group.append(types.InputMediaVideo(media=media_id))
                    elif (media_type == 'document'):
                        media_group.append(types.InputMediaDocument(media=media_id))

            await message.bot.send_media_group(chat_id=chat_id, media=media_group)
            message = await message.answer(f'📅 Date: {forward_date}\n⏰ Time: {forward_time}', reply_markup=tasks_buttons)

            cursor.execute('UPDATE tasks SET message_id_to_edit=%s WHERE user_id=%s AND message_id=%s', (message.message_id - 1, chat_id, message_id))
            sqlite_connection.commit()

    if (len(all_tasks) == 0):
        message = await message.answer('💤 No tasks')

def register_handlers_tasks(dp: Dispatcher):
    dp.register_message_handler(tasks, commands="tasks", state="*")
