"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_product_by_id(product_id):
    """Возвращает объект Product по его id (или None)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return Product(
        product_id=row[0],
        category=row[1],
        name=row[2],
        weight=row[3],
        price=row[4],
        quantity=row[5],
        image=row[6],
    )


def get_all_orders():
    """Возвращает список объектов Order из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент, товар_id, количество FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        order_id, date, client, product_id, quantity = row
        product = get_product_by_id(product_id)
        if product is None:
            continue  # на случай битой ссылки
        orders.append(Order(order_id, date, client, product, quantity))
    return orders


def print_orders(orders):
    """Выводит информацию о заказах."""
    print(f"\nВсего заказов: {len(orders)}\n")
    total_sum = 0
    for o in orders:
        print(o.info())
        total_sum += o.total()
    print("-" * 60)
    print(f"Итого по всем заказам: {total_sum} руб.")


if __name__ == "__main__":
    orders = get_all_orders()
    print_orders(orders)