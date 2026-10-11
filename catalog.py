"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from config import DB_PATH, COLOR_HIGHLIGHT, FONT_FAMILY
import db_products as db          


def create_product_card(parent, product):
    # Получаем количество и вычисляем цвет фона
    qty = product.quantity
    bg_color = "#ff8080" if qty <= 3 else "#FFFFFF"

    # Карточка
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", pady=4, padx=4)

    # Изображение (если есть)
    img_frame = tk.Frame(card, bg=bg_color, width=110, height=110)
    img_frame.pack(side="left", padx=10, pady=10)
    img_frame.pack_propagate(False)

    try:
        img = Image.open(f"resources/{product.image}").resize((100, 100))
        img_photo = ImageTk.PhotoImage(img)
        tk.Label(img_frame, image=img_photo, bg=bg_color).pack()
        # сохраняем ссылку, чтобы не собрал GC
        img_frame.image = img_photo
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # Текстовая часть справа
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(text_frame, text=f"{product.category} | {product.name}",
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {product.category}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Вес: {product.weight}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"{product.price} руб.",
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="e").pack(fill="x")

    # Разделитель снизу карточки
    separator = tk.Frame(parent, height=1, bg="#70B2AF")
    separator.pack(fill="x", pady=(5, 0))

    return card