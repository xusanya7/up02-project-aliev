"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)   # дата расчёта → прошлый месяц = сентябрь 2026

    # id, цена, ожидание, пояснение
    test_cases = [
        (1, 700.0, 700.0, "Пепперони — есть заказы → ,без скидки"),
        (2, 750.0, 750.0, "Калифорния — есть заказы → без скидки"),
        (3, 350.0, 350.0, "Гамбургер — есть заказы → без скидки"),
        (4, 400.0, 300.0, "Греческий — нет заказов → −25%"),
        (5, 500.0, 375.0, "Болоньезе — нет заказов → −25%"),
        (6, 350.0, 262.5, "Чизкейк — нет заказов → −25%"),
        (7, 100.0, 75.0,  "Кола — нет заказов → −25%"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()