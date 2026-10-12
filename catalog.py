"""Каталог товаров."""
import tkinter as tk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import load_image_proportional


def create_product_card(parent, product):
    """Создаёт карточку товара."""
    bg = _get_card_color(product.quantity)

    card = tk.Frame(parent, bg=bg, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg)
    _add_text_info(card, product, bg)

    return card


def _get_card_color(qty):
    """Цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg):
    """Изображение товара или заглушка."""
    frame = tk.Frame(card, bg=bg)
    frame.pack(side="left", padx=10, pady=10)

    photo = load_image_proportional(f"resources/{product.image}",
                                    max_size=(100, 100))
    if photo:
        lbl = tk.Label(frame, image=photo, bg=bg)
        lbl.image = photo
        lbl.pack()
    else:
        tk.Label(frame, text="[НЕТ ФОТО]", bg=bg,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg):
    """Текстовая информация о товаре."""
    frame = tk.Frame(card, bg=bg)
    frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    name     = product.name     or "[Без названия]"
    category = product.category or "[Без категории]"
    weight   = product.weight   if product.weight   is not None else 0
    price    = product.price    if product.price    is not None else 0
    qty      = product.quantity if product.quantity is not None else 0

    _add_label(frame, name, bg, bold=True, size=FONT_SIZE_HEADER)
    _add_label(frame, f"Категория: {category}", bg)
    _add_label(frame, f"Количество: {_indicator(qty)} ({qty})", bg)
    _add_label(frame, f"Вес: {weight} г", bg)
    _add_label(frame, f"{price} руб.", bg, bold=True,
               size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Метка с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg, anchor=align).pack(fill="x")


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    return "много" if qty > 5 else "мало"