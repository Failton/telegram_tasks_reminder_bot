from ..utils.create_db import create_db

import asyncio

from datetime import datetime
from time import time

from aiogram import Bot

sqlite_connection = create_db()

def form_offset(num):
    offset = ''

    if (num < 0):
        num *= -1
        offset += '-'
    else:
        offset += '+'

    if (num < 600):
        offset += '0'

    offset += str(num // 60)
    if (num % 60 != 0):
        if (num % 60 < 10):
            offset += '0'
        offset += str(num % 60)
    else:
        offset += '00'

    return (offset)


async def check_for_tasks(bot: Bot):
    while True:
        cursor = sqlite_connection.cursor()
        cursor.execute('SELECT * FROM tasks')
        all_tasks = cursor.fetchall()

        for task in all_tasks:
            forward_date = task[3]
            forward_time = task[4]

            if (forward_date != ' ' and forward_time != ' '):
                chat_id = task[1]
                offset = form_offset(int(task[2]))
                message_id = task[5]
                media_group_id = task[7]
                media_ids = task[8].split('|')
                time_sec = datetime.strptime(f'{forward_date} {forward_time} {offset}', '%d/%m/%Y %H:%M:%S %z').timestamp()

                if (time_sec <= time()):
                    if (media_group_id == ' '):
                        await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
                    else:
                        media_group = []

                        for media in media_ids:
                            media_type, media_id = media.split(':')
                            if (media_type == 'photo'):
                                media_group.append(types.InputMediaPhoto(media=media_id))
                            elif (media_type == 'video'):
                                media_group.append(types.InputMediaVideo(media=media_id))
                            elif (media_type == 'document'):
                                media_group.append(types.InputMediaDocument(media=media_id))

                        await bot.send_media_group(chat_id=chat_id, media=media_group)

                    cursor.execute('DELETE FROM tasks WHERE user_id=%s AND message_id=%s', (chat_id, message_id))
                    sqlite_connection.commit()
        await asyncio.sleep(1)
