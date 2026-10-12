"""Загрузка товаров из БД."""
import sqlite3
from config import DB_PATH
from models import Product


def row_to_product(row):
    return Product(
        product_id=row[0],                    # id
        category="—",                         # категории в БД нет
        name=row[1],                          # название
        weight=row[2],                        # вес
        price=row[3],                         # цена
        quantity=row[4],                      # количество
        image=row[5],                         # фото
        description=row[6] if len(row) > 6 else None,  # description
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

def get_product_sizes(product_id):
    """
    Возвращает список размеров для товара.
    :param product_id: id товара
    :return: список размеров
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT размер FROM Товар WHERE id = ?", (product_id,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows if row[0]]