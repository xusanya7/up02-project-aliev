"""Админ-панель (заглушка)."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)


class AdminPanel:
    """Окно админ-панели."""

    def __init__(self, parent, current_user=None):
        self.current_user = current_user
        self.window = tk.Toplevel(parent)
        self.window.title("Админ-панель")
        self.window.geometry("600x400")
        self.window.configure(bg=COLOR_MAIN_BG)

        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="АДМИН-ПАНЕЛЬ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        if current_user:
            fio = f"{current_user[1]} {current_user[2]}"
            tk.Label(self.window,
                     text=f"Вы вошли как: {fio} ({current_user[5]})",
                     font=font(FONT_SIZE_NORMAL),
                     bg=COLOR_MAIN_BG).pack(pady=10)

        tk.Label(self.window,
                 text="Здесь будет управление товарами",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(pady=30)

        tk.Button(self.window, text="Закрыть",
                  command=self.window.destroy,
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(pady=10)