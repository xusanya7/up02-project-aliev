"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)

        # --- Базовая серия: дата 15.10.2026, прошлый месяц — сентябрь ---
        (1, 700.0, datetime(2026, 10, 15), 700.0, "Пепперони — есть заказ в сентябре → без скидки"),
        (2, 750.0, datetime(2026, 10, 15), 750.0, "Калифорния — есть заказ в сентябре → без скидки"),
        (3, 350.0, datetime(2026, 10, 15), 350.0, "Гамбургер — есть заказ в сентябре → без скидки"),
        (4, 400.0, datetime(2026, 10, 15), 300.0, "Греческий — нет заказов → −25%"),
        (5, 500.0, datetime(2026, 10, 15), 375.0, "Болоньезе — нет заказов → −25%"),
        (6, 350.0, datetime(2026, 10, 15), 262.5, "Чизкейк — нет заказов → −25%"),
        (7, 100.0, datetime(2026, 10, 15), 75.0,  "Кола — нет заказов → −25%"),

        # --- Граничные случаи ---
        (4, 400.0, datetime(2026, 9, 1),  300.0, "01.09 → прошлый месяц август, заказов нет → −25%"),
        (2, 750.0, datetime(2026, 10, 31), 750.0, "31.10 → прошлый месяц сентябрь, заказ есть → без скидки"),
        (1, 700.0, datetime(2026, 11, 15), 525.0, "15.11 → прошлый месяц октябрь, заказов нет → −25%"),
    ]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()