"""Расширенная проверка каталога товаров."""
import db_products as db


def test_fields():
    """Проверяет, что у всех товаров есть обязательные поля."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required = ["id", "category", "name", "weight", "price", "quantity", "image"]
    errors = 0

    for p in products:
        for field in required:
            if not hasattr(p, field):
                print(f"❌ Товар id={p.id}: нет поля '{field}'")
                errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_prices():
    """У всех товаров есть цена (не None)."""
    products = db.get_all_products()
    for p in products:
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            return
    print("✅ У всех товаров есть цена")


def test_quantity():
    """Количество у всех товаров ≥ 0."""
    products = db.get_all_products()
    for p in products:
        if p.quantity is None or p.quantity < 0:
            print(f"❌ Товар id={p.id}: некорректное количество ({p.quantity})")
            return
    print("✅ У всех товаров количество ≥ 0")


def test_images():
    """Хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    for p in products:
        if p.image:
            print(f"✅ Есть товар с изображением (id={p.id}, {p.image})")
            return
    print("❌ Ни у одного товара нет изображения")


if __name__ == "__main__":
    test_fields()
    test_prices()
    test_quantity()
    test_images()