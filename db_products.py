"""Загрузка товаров из БД."""
import sqlite3
from config import DB_PATH
from models import Product


def row_to_product(row):
    return Product(
        product_id=row[0],
        category=row[1],
        name=row[2],
        weight=row[3],
        price=row[4],
        quantity=row[5],
        image=row[6],
    )


def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [row_to_product(r) for r in rows]


def get_products_by_category(category):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ? ORDER BY id", (category,))
    rows = cur.fetchall()
    conn.close()
    return [row_to_product(r) for r in rows]