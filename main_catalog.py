"""Главное окно приложения."""
import tkinter as tk
from tkinter import messagebox

from styles import COLOR_MAIN_BG, font, FONT_SIZE_HEADER
from catalog import create_product_card
from db_products import get_all_products
from order_manager import create_order


class MainApp:
    """Главное окно каталога."""

    def __init__(self, root):
        self.root = root
        self.root.title("Каталог товаров")
        self.root.geometry("800x600")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.cart = []   # корзина: список словарей

        self.build_ui()
        self.load_products()

    def build_ui(self):
        tk.Label(self.root, text="Каталог товаров",
                 font=font(FONT_SIZE_HEADER, bold=True),
                 bg=COLOR_MAIN_BG).pack(pady=10)

        tk.Button(self.root, text="Оформить заказ",
                  command=self.checkout).pack(pady=5)

        self.catalog_frame = tk.Frame(self.root, bg=COLOR_MAIN_BG)
        self.catalog_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_products(self):
        products = get_all_products()
        for product in products:
            create_product_card(self.catalog_frame, product,
                                refresh=self.add_to_cart)

    def refresh_catalog(self):
        """Удаляет старые карточки и загружает заново."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def add_to_cart(self, product, qty, size):
        """Callback из формы: добавляет товар в корзину."""
        self.cart.append({
            "product_id": product.id,
            "size": size,
            "quantity": qty,
            "price": product.price,
        })
        print(f"[КОРЗИНА] {self.cart}")

    def checkout(self):
        """Оформляет заказ со всеми позициями корзины."""
        if not self.cart:
            messagebox.showwarning("Корзина", "Корзина пуста")
            return

        items = [(i["product_id"], i["size"], i["quantity"], i["price"])
                 for i in self.cart]

        order_id = create_order("Петров Петр", items)

        if order_id:
            messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
            self.cart = []
            self.refresh_catalog()
        else:
            messagebox.showerror("Ошибка", "Не удалось оформить заказ")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()