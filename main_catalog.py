"""Главное окно приложения."""
import tkinter as tk
from tkinter import messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from catalog import create_product_card
from db_products import get_all_products
from order_manager import create_order


class MainApp:
    """Главное окно каталога."""

    def __init__(self, root, user):
        """
        :param root: главное окно Tk
        :param user: словарь {'id', 'login', 'role'}
        """
        self.root = root
        self.current_user = user

        self.root.title(f"Каталог товаров — {user['login']} ({user['role']})")
        self.root.geometry("800x600")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.cart = []

        self.build_ui()
        self.load_products()

    # ---------- UI ----------

    def build_ui(self):
        """Строит интерфейс главного окна."""
        header = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        header.pack(fill="x", pady=10)

        tk.Label(header, text="Каталог товаров",
                 font=font(FONT_SIZE_HEADER, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=20)

        # Кнопка «Оформить заказ» — всем
        tk.Button(header, text="Оформить заказ",
                  command=self.checkout,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=10)

        # Кнопка «Заказы» — manager и admin
        if self.current_user["role"] in ("manager", "admin"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

        # Кнопка «Управление товарами» — только admin
        if self.current_user["role"] == "admin":
            tk.Button(header, text="Управление товарами",
                      command=self.open_products_admin,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

        # Кнопка «Выйти» — всем
        tk.Button(header, text="Выйти",
                  command=self.logout,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=10)

        # Контейнер для карточек
        self.catalog_frame = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        self.catalog_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------- Каталог ----------

    def load_products(self):
        for product in get_all_products():
            create_product_card(self.catalog_frame, product,
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

    # ---------- Заказ ----------

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина", "Корзина пуста")
            return

        items = [(i["product_id"], i["size"], i["quantity"], i["price"])
                 for i in self.cart]

        order_id = create_order(self.current_user["login"], items)

        if order_id:
            messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
            self.cart = []
            self.refresh_catalog()
        else:
            messagebox.showerror("Ошибка", "Не удалось оформить заказ")

    # ---------- Доступ по ролям ----------

    def open_orders(self):
        """Открывает окно списка заказов (manager, admin)."""
        if self.current_user["role"] not in ("manager", "admin"):
            messagebox.showerror("Доступ запрещён", "Нет прав")
            return
        from orders_window import OrdersWindow
        OrdersWindow(self.root)

    def open_products_admin(self):
        """Открывает окно управления товарами (только admin)."""
        if self.current_user["role"] != "admin":
            messagebox.showerror("Доступ запрещён", "Нет прав")
            return

        messagebox.showinfo("В разработке",
                            "Окно управления товарами будет позже")

    # ---------- Выход ----------

    def logout(self):
        """Выход: закрывает каталог и снова показывает окно входа."""
        if not messagebox.askyesno("Выход", "Выйти из системы?"):
            return

        self.root.destroy()
        root = tk.Tk()
        root.withdraw()
        from login_window import LoginWindow
        LoginWindow(root, on_success=lambda user: start_main(root, user))
        root.mainloop()


# ---------- Точка входа ----------

def start_main(root, user):
    """Запускает главное окно после успешного входа."""
    root.deiconify()
    MainApp(root, user)


if __name__ == "__main__":
    from login_window import LoginWindow

    root = tk.Tk()
    root.withdraw()   # прячем пустое главное окно до входа

    def on_login_success(user):
        start_main(root, user)

    LoginWindow(root, on_success=on_login_success)
    root.mainloop()