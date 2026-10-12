"""Работа с БД: пользователи, роли, товары."""

import sqlite3

DB_PATH = "databases/db_variant_15.db"


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_user_by_login(login):
    """
    Ищет пользователя по логину.
    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """,
        (login,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_all_users():
    """
    Возвращает список всех пользователей.
    :return: список кортежей (id, фамилия, имя, логин, роль)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_products():
    """
    Возвращает все товары из БД.
    :return: список объектов Product
    """
    from db_products import get_all_products as _get

    return _get()
