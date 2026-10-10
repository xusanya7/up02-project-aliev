"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар (вариант 15: еда)."""

    def __init__(self, product_id, category, name, weight, price, quantity, image):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param category: категория (Пицца, Суши, …)
        :param name: название
        :param weight: вес, г
        :param price: цена, руб.
        :param quantity: остаток на складе
        :param image: имя файла фото
        """
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

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )