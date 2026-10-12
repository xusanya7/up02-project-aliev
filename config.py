"""Конфигурация приложения."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "databases", "db_variant_15.db")

# Название приложения (для заголовка окна)
APP_TITLE = "Каталог товаров"
TITLE = "Каталог товаров"
FONT = "Calibri"

# Путь к базе данных
DB_PATH = "databases/db_variant_15.db"

# Шрифт интерфейса
FONT_FAMILY = "Calibri"

# Цвета (по КИМ)
COLOR_BG = "#FFFFFF"  # основной фон
COLOR_HEADER = "#D2F6E7"  # шапка / дополнительный фон
COLOR_ACCENT = "#70B2AF"  # акцент (разделители)
COLOR_HIGHLIGHT = "#ff8080"  # подсветка при количестве ≤3

# Размеры окна
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
