"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (вариант 15: еда)."""
    
    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо)."""
        return self.price * 0.80 # изменено в ветке conflict-test

    def __init__(self, product_id, category, name, weight, price, quantity, image):
        self.id = product_id
        self.category = category
        self.name = name
        self.weight = weight
        self.price = price
        self.quantity = quantity
        self.image = image

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def price_with_discount(self, discount_percent):
        """Цена с указанной скидкой в процентах (ручной режим)."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """True, если товар есть в наличии."""
        return self.quantity > 0

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity

    def info(self):
        return (
            f"Заказ №{self.id} от {self.date}: "
            f"{self.client} — {self.product.name} × {self.quantity} "
            f"= {self.total()} руб."
        )