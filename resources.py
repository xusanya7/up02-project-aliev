"""Модуль работы с ресурсами."""

import os
from PIL import Image, ImageTk

PATH_PICTURE = "assets/picture.png"
PATH_LOGO = "assets/logo.png"
PATH_ICON = "assets/icon.ico"

_image_cache = {}


from PIL import Image, ImageDraw, ImageTk


def create_placeholder(size=(200, 200), text="Нет фото"):
    """Создаёт заглушку с текстом, если файла нет."""
    img = Image.new("RGB", size, "#E0E0E0")
    draw = ImageDraw.Draw(img)
    # рамка
    draw.rectangle([0, 0, size[0] - 1, size[1] - 1], outline="#AAAAAA", width=2)
    # текст по центру
    bbox = draw.textbbox((0, 0), text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill="#666666")
    return ImageTk.PhotoImage(img)


def load_image(path, size=(100, 100)):
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None


def load_image_proportional(path, max_size=(100, 100)):
    """
    Загружает изображение с сохранением пропорций.
    Используется для логотипа.
    """
    try:
        if not os.path.exists(path):
            return create_placeholder(max_size)
        img = Image.open(path)
        img.thumbnail(max_size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return create_placeholder(max_size)
