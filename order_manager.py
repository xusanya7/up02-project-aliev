import sqlite3
from datetime import datetime

DB_PATH = "databases/db_variant_15.db"


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_product_quantity(product_id):
    """
    Возвращает количество товара по id.
    :param product_id: id товара
    :return: количество (int)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def decrease_product_quantity(product_id, quantity):
    """
    Уменьшает количество товара на складе.
    :param product_id: id товара
    :param quantity: на сколько уменьшить
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Проверяем, что товара достаточно
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False

        current = row[0]
        if current < quantity:
            return False

        # Уменьшаем
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (quantity, product_id)
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления: {e}")
        return False

    finally:
        conn.close()


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заказ
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции И уменьшаем остатки
        for product_id, size, quantity, price in items:
            # Проверяем наличие
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")

            # Добавляем позицию
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, размер, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )

            # Уменьшаем остаток
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )

        # 3. Фиксируем ВСЁ
        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()

def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_items(order_id):
    """
    Возвращает состав заказа.
    :param order_id: id заказа
    :return: список кортежей (id, название, размер, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.название,
               Состав_заказа.размер, Состав_заказа.количество,
               Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows