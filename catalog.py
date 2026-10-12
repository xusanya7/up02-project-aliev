"""Каталог товаров."""

import tkinter as tk

from styles import (
    COLOR_MAIN_BG,
    COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL,
    FONT_SIZE_HEADER,
    font,
)
from resources import load_image_proportional


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку товара по макету."""
    bg = _get_card_color(product.quantity)

    card = tk.Frame(parent, bg=bg, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg)
    _add_text_info(card, product, bg)

    # Привязка клика ко ВСЕМ виджетам карточки
    def on_click(e):
        _open_view(parent, product, refresh)

    card.bind("<Button-1>", on_click)
    _bind_recursive(card, on_click)

    return card


def _bind_recursive(widget, handler):
    """Рекурсивно привязывает клик ко всем дочерним виджетам."""
    for child in widget.winfo_children():
        child.bind("<Button-1>", handler)
        _bind_recursive(child, handler)


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg):
    """Добавляет изображение товара или заглушку."""
    frame = tk.Frame(card, bg=bg)
    frame.pack(side="left", padx=10, pady=10)

    photo = None
    if product.image:
        photo = load_image_proportional(
            f"resources/{product.image}", max_size=(100, 100)
        )

    if photo:
        lbl = tk.Label(frame, image=photo, bg=bg)
        lbl.image = photo
        lbl.pack()
    else:
        tk.Label(frame, text="[НЕТ ФОТО]", bg=bg, width=10, height=5).pack()


def _add_text_info(card, product, bg):
    """Добавляет текстовую информацию о товаре."""
    frame = tk.Frame(card, bg=bg)
    frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    name = _truncate(product.name) or "[Без названия]"
    category = _truncate(product.category) or "[Без категории]"
    weight = product.weight if product.weight is not None else 0
    qty = product.quantity if product.quantity is not None else 0
    price = _format_price(product.price)

    _add_label(frame, name, bg, bold=True, size=FONT_SIZE_HEADER)
    _add_label(frame, f"Категория: {category}", bg)
    _add_label(frame, f"Количество: {_indicator(qty)} ({qty})", bg)
    _add_label(frame, f"Вес: {weight} г", bg)
    _add_label(frame, price, bg, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg, anchor=align).pack(
        fill="x"
    )


def _indicator(qty):
    try:
        qty = float(qty)
    except (TypeError, ValueError):
        return "мало"
    return "много" if qty > 5 else "мало"


def _format_price(price):
    if price is None:
        price = 0
    return f"{int(price):,} руб.".replace(",", " ")


def _truncate(text, max_len=100):
    if not text:
        return text
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


def _open_view(parent, product, refresh=None):
    """Открывает форму просмотра товара."""
    try:
        from view_form import ViewForm

        ViewForm(parent, product, on_add_to_order=refresh)
    except Exception as e:
        print(f"[ОШИБКА открытия формы] {e}")
        from tkinter import messagebox

        messagebox.showerror("Ошибка формы", str(e))
