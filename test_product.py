"""Проверка класса Product."""

from models import Product

p = Product(
    product_id=1,
    category="Пицца",
    name="Пепперони",
    weight=450,
    price=750,
    quantity=3,
    image="pepperoni.jpg",
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
