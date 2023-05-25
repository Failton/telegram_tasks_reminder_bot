from ..utils.create_db import create_db

from aiogram import Dispatcher, types


sqlite_connection = create_db()


async def button_delete(callback_query: types.CallbackQuery):
    cursor = sqlite_connection.cursor()

    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    cursor.execute('SELECT media_ids FROM tasks WHERE user_id=%s AND message_id_to_edit=%s', (chat_id, message_id - 1))
    num_of_legends = len(cursor.fetchone()[0].split('|'))

    for i in range(num_of_legends):
        await callback_query.bot.delete_message(chat_id=chat_id, message_id=(message_id - 1 - i))
    await callback_query.bot.edit_message_text(chat_id=chat_id, message_id=(message_id), text='❌ Deleted!')

    cursor.execute('DELETE FROM tasks WHERE user_id=%s AND message_id_to_edit=%s', (chat_id, message_id - 1))
    sqlite_connection.commit()


def register_handlers_button_delete(dp: Dispatcher):
    dp.register_callback_query_handler(button_delete, text="button_delete")
