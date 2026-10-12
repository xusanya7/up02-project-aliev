"""Каталог товаров."""
import tkinter as tk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import load_image_proportional


#  Главная функция — карточка товара
def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    bg = _get_card_color(product.quantity)

    card = tk.Frame(parent, bg=bg, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg)
    _add_text_info(card, product, bg)

    return card



#  Цвет карточки (подсветка при qty ≤ 3)
def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


#
#  Изображение (или заглушка)
#
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
        lbl.image = photo          # сохраняем ссылку!
        lbl.pack()
    else:
        tk.Label(frame, text="[НЕТ ФОТО]", bg=bg,
                 width=10, height=5).pack()



#  Текстовая информация о товаре
def _add_text_info(card, product, bg):
    """Добавляет текстовую информацию о товаре."""
    frame = tk.Frame(card, bg=bg)
    frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Обработка крайних случаев
    name     = _truncate(product.name)     or "[Без названия]"
    category = _truncate(product.category) or "[Без категории]"
    weight   = product.weight   if product.weight   is not None else 0
    qty      = product.quantity if product.quantity is not None else 0
    price    = _format_price(product.price)

    # Метки 
    _add_label(frame, name, bg, bold=True, size=FONT_SIZE_HEADER)
    _add_label(frame, f"Категория: {category}", bg)
    _add_label(frame, f"Количество: {_indicator(qty)} ({qty})", bg)
    _add_label(frame, f"Вес: {weight} г", bg)
    _add_label(frame, price, bg, bold=True,
               size=FONT_SIZE_HEADER, align="e")

#  Универсальная метка

def _add_label(parent, text, bg, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg, anchor=align).pack(fill="x")

#  Индикатор «много / мало» (порог 5)
def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    try:
        qty = float(qty)         # приведём к числу
    except (TypeError, ValueError):
        return "мало"            # на плохих данных — «мало»
    return "много" if qty > 5 else "мало"

#  Форматирование цены (1 500 000 руб.)

def _format_price(price):
    """Форматирует цену: 1 500 000 руб."""
    if price is None:
        price = 0
    return f"{int(price):,} руб.".replace(",", " ")


#  Обрезка длинного текста (> 100 символов)

def _truncate(text, max_len=100):
    """Обрезает длинный текст с многоточием."""
    if not text:
        return text
    return text if len(text) <= max_len else text[:max_len - 3] + "..."

def _format_price(price):
    """Форматирует цену: 1 500 000 руб."""
    if price is None:
        price = 0
    return f"{int(price):,} руб.".replace(",", " ")


def _truncate(text, max_len=100):
    """Обрезает длинный текст с многоточием."""
    if not text:
        return text
    return text if len(text) <= max_len else text[:max_len - 3] + "..."