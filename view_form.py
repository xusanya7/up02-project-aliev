"""Форма просмотра товара с выбором размера и количества."""

import tkinter as tk
from tkinter import ttk, messagebox

from styles import COLOR_MAIN_BG, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
from error_handler import validate_positive_int
from order_manager import get_product_quantity


class ViewForm:
    """Окно просмотра товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        """
        :param parent: родительское окно
        :param product: объект Product
        :param on_add_to_order: callback(product, qty, size)
        """
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр товара")
        self.window.geometry("400x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # === Название ===
        tk.Label(
            main,
            text=self.product.name,
            font=font(FONT_SIZE_HEADER, bold=True),
            bg=COLOR_MAIN_BG,
        ).pack(anchor="w")

        # === Информация о товаре ===
        info = tk.Frame(main, bg=COLOR_MAIN_BG)
        info.pack(fill="x", pady=10)

        tk.Label(
            info,
            text=f"Цена: {self.product.price} руб.",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_MAIN_BG,
        ).pack(anchor="w")
        tk.Label(
            info,
            text=f"На складе: {get_product_quantity(self.product.id)} шт.",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_MAIN_BG,
        ).pack(anchor="w")

        # === Поле ввода количества ===
        qty_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)

        tk.Label(
            qty_frame, text="Количество:", font=font(FONT_SIZE_NORMAL), bg=COLOR_MAIN_BG
        ).pack(side="left", padx=5)

        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(
            qty_frame, textvariable=self.qty_var, width=5, font=font(FONT_SIZE_NORMAL)
        )
        qty_entry.pack(side="left", padx=5)

        # === Выбор размера ===
        size_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=10)

        tk.Label(
            size_frame, text="Размер:", font=font(FONT_SIZE_NORMAL), bg=COLOR_MAIN_BG
        ).pack(side="left", padx=5)

        sizes = self._get_sizes()
        if not sizes:
            sizes = ["—"]

        self.size_var = tk.StringVar(value=sizes[0])
        size_combo = ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=sizes,
            state="readonly",
            width=5,
            font=font(FONT_SIZE_NORMAL),
        )
        size_combo.pack(side="left", padx=5)

        # === Кнопка «Добавить в заказ» ===
        tk.Button(
            main,
            text="Добавить в заказ",
            font=font(FONT_SIZE_NORMAL),
            command=self.add_to_order,
        ).pack(pady=20)

    def _get_sizes(self):
        """Возвращает список размеров для товара."""
        try:
            from db_products import get_product_sizes

            return get_product_sizes(self.product.id)
        except Exception as e:
            print(f"[Размеры] {e}")
            return []

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        # 1. Проверяем товар
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 2. Валидация количества
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return

        qty = result

        # 3. Проверяем остаток
        current_qty = get_product_quantity(self.product.id)
        if qty > current_qty:
            messagebox.showwarning("Ошибка", f"Доступно только {current_qty} шт.")
            return

        # 4. Вызываем callback
        try:
            if self.on_add_to_order:
                self.on_add_to_order(self.product, qty, self.size_var.get())

            messagebox.showinfo("Успех", f"Товар добавлен в заказ ({qty} шт.)")
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить товар:\n{e}")
