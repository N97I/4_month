import sqlite3
from db import queries

DB_NEW = "todo.db"


def init_db():
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.CREATE_TABLE_TASKS)
        conn.commit()


def get_tasks(sort_by_date_desc=True, sort_by_status=False):
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        query = queries.SELECT_TASKS
        if sort_by_status:
            query += " ORDER BY completed ASC, created_at " + ("DESC" if sort_by_date_desc else "ASC")
        else:
            query += " ORDER BY created_at " + ("DESC" if sort_by_date_desc else "ASC")
        cursor.execute(query)
        return cursor.fetchall()


def add_task(task):
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.INSERT_TASK, (task,))
        conn.commit()


def update_task(task_id, new_text):
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.UPDATE_TASK, (new_text, task_id))
        conn.commit()


def update_task_status(task_id, completed):
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.UPDATE_TASK_STATUS, (int(completed), task_id))
        conn.commit()


def delete_task(task_id):
    with sqlite3.connect(DB_NEW) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.DELETE_TASK, (task_id,))
        conn.commit()