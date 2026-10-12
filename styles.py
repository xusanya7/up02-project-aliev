"""Стили приложения."""
import tkinter as tk
from tkinter import font as tkfont

# Цвета
COLOR_MAIN_BG = "#FFFFFF"
COLOR_SECONDARY_BG = "#F0F0F0"
COLOR_ACCENT = "#007BFF"
COLOR_HIGHLIGHT = "#FFEEAA"

# Размеры шрифтов
FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 14
FONT_SIZE_TITLE = 18


def font(size, bold=False):
    return ("Arial", size, "bold" if bold else "normal")