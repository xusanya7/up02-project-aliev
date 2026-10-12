"""Главное окно приложения."""
import tkinter as tk
from tkinter import ttk, messagebox

import database as db
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from auth import AuthWindow
from admin_panel import AdminPanel
from catalog import create_product_card
from config import APP_TITLE


class MainWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.current_user = None
        self.user_label = None
        self.cart = []

        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", expand=True)

        # Кнопка «Оформить заказ» — всем
        tk.Button(header, text="Оформить заказ",
                  command=self.checkout,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=10)

        # ФИО пользователя (правый верхний угол)
        self.user_label = tk.Label(header, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

        # Каталог с прокруткой
        self.canvas = tk.Canvas(self.root, bg="white",
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def require_auth(self):
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        self.current_user = user

        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        self.user_label.config(text=f"{fio} ({user[5]})")

        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        header = self.user_label.master

        if role in ("Менеджер", "Администратор"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

        if role == "Администратор":
            tk.Button(header, text="Админ-панель",
                      command=self.open_admin,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

    def open_orders(self):
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        AdminPanel(self.root, self.current_user)

    def load_products(self):
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p,
                                refresh=self.add_to_cart)

    def refresh_catalog(self):
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def add_to_cart(self, product, qty, size):
        self.cart.append({
            "product_id": product.id,
            "size": size,
            "quantity": qty,
            "price": product.price,
        })
        print(f"[КОРЗИНА] {self.cart}")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина", "Корзина пуста")
            return

        from order_manager import create_order

        client = f"{self.current_user[1]} {self.current_user[2]}"
        items = [(i["product_id"], i["size"], i["quantity"], i["price"])
                 for i in self.cart]

        order_id = create_order(client, items)

        if order_id:
            messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
            self.cart = []
            self.refresh_catalog()
        else:
            messagebox.showerror("Ошибка", "Не удалось оформить заказ")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()