"""Проверка полей товаров."""
import db_products as db


def test_fields():
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required = ["id", "name", "category", "price", "quantity", "image"]
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


if __name__ == "__main__":
    test_fields()