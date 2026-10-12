"""Главное окно с каталогом."""
import tkinter as tk
from tkinter import ttk

from styles import COLOR_SECONDARY_BG, FONT_SIZE_TITLE, font
from config import APP_TITLE
import db_products as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from error_handler import safe_call


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.set_icon()
        self.build_ui()
        self.load_products()

    def set_icon(self):
        import os
        try:
            if os.name == "nt":
                self.root.iconbitmap(PATH_ICON)
            else:
                icon_img = load_image_proportional(
                    PATH_ICON.replace(".ico", ".png"), max_size=(32, 32)
                )
                if icon_img:
                    self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                   command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Загружает товары с обработкой ошибок."""
        products = safe_call(db.get_all_products) or []
        for p in products:
            safe_call(create_product_card,
                      self.catalog_frame, p,
                      refresh=self.refresh_catalog)

    def refresh_catalog(self):
        """Обновляет каталог (пересоздаёт карточки)."""
        for w in self.catalog_frame.winfo_children():
            w.destroy()
        self.load_products()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CatalogWindow()
    app.run()