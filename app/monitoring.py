import sqlite3
from datetime import datetime


def log_login_attempt(user_id, username, result):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO login_attempts
        (user_id, username, result, date_time)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, username, result, date_time)
    )

    connection.commit()
    connection.close()


def get_login_history(user_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT date_time, result
        FROM login_attempts
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    attempts = cursor.fetchall()

    connection.close()

    return attempts