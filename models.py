"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар (вариант 15: еда)."""

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

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """True, если товар есть в наличии (количество > 0)."""
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
        """
        :param order_id: идентификатор заказа
        :param date: дата заказа
        :param client: ФИО клиента
        :param product: объект класса Product
        :param quantity: количество товара в заказе
        """
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product
        self.quantity = quantity

    def total(self):
        """Стоимость заказа."""
        return self.product.price * self.quantity

    def info(self):
        """Строка с информацией о заказе."""
        return (
            f"Заказ №{self.id} от {self.date}: "
            f"{self.client} — {self.product.name} × {self.quantity} "
            f"= {self.total()} руб."
        )