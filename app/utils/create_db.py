import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="",
                                  port="",
                                  database='tg_tasks_reminder_bot_db')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                   user_num SERIAL PRIMARY KEY,
                   user_id DECIMAL,
                   utc_offset INT,
                   block INT
                   );''')
    connection.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                   task_id SERIAL PRIMARY KEY,
                   user_id DECIMAL,
                   utc_offset INT,
                   date TEXT,
                   time TEXT,
                   message_id DECIMAL,
                   message_id_to_edit DECIMAL,
                   media_group_id TEXT,
                   media_ids TEXT,
                   caption TEXT
                   );''')
    connection.commit()
    return connection
