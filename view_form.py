"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image_proportional
from error_handler import safe_call, validate_positive_int
from order_manager import (
    add_order_to_db, update_product_quantity, get_product_quantity
)


class ViewForm:
    """Форма просмотра выбранного товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.name}")
        self.window.geometry("700x650")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)

        photo = None
        if self.product.image:
            photo = safe_call(
                load_image_proportional,
                f"resources/{self.product.image}",
                max_size=(200, 200)
            )
        if photo:
            lbl = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            lbl.image = photo
            lbl.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]",
                     bg=COLOR_MAIN_BG, width=20, height=10).pack()

        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Наименование", self.product.name)
        self._add_field(info_frame, "Категория",    self.product.category)
        self._add_field(info_frame, "Вес",          f"{self.product.weight} г")
        self._add_field(info_frame, "Цена",         f"{self.product.price} руб.")
        self._add_field(info_frame, "Количество",   self.product.quantity)

        desc = getattr(self.product, "description", None) or "—"
        self._add_field(info_frame, "Описание", desc)

        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(qty_frame, text="Количество:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left")
        self.qty_entry = tk.Entry(qty_frame, width=10,
                                  font=font(FONT_SIZE_NORMAL))
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=10)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Добавить N шт.",
                  command=self.add_qty_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")
        tk.Label(row, text=str(value),
                 font=font(FONT_SIZE_NORMAL),
                 anchor="w", wraplength=300, justify="left",
                 bg=COLOR_MAIN_BG).pack(side="left")

    def add_to_order(self):
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        try:
            pid = self.product.id
            current_qty = get_product_quantity(pid)
            if current_qty < 1:
                messagebox.showwarning("Нет в наличии", "Товар закончился")
                return
            new_qty = current_qty - 1
            add_order_to_db("Иванов Иван Иванович", pid, 1)
            update_product_quantity(pid, new_qty)
            messagebox.showinfo("Успех", "Заказ оформлен")
            if self.on_add_to_order:
                self.on_add_to_order()
        except Exception as e:
            messagebox.showerror("Ошибка заказа", str(e))

    def add_qty_to_order(self):
        ok, result = validate_positive_int(self.qty_entry.get(), "Количество")
        if not ok:
            messagebox.showerror("Ошибка ввода", result)
            return
        qty = result
        if qty > self.product.quantity:
            messagebox.showwarning("Мало на складе",
                                   f"Доступно только {self.product.quantity} шт.")
            return
        if not self.on_add_to_order:
            messagebox.showinfo("Информация", "Функция в разработке")
            return
        try:
            for _ in range(qty):
                self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", f"Добавлено {qty} шт.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))