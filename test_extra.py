"""Дополнительные тесты алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def check(product_id, price, date, expected, comment):
    """Одна проверка."""
    result = calculate_price_with_discount(product_id, price, date)
    status = "✅" if result == expected else "❌"
    print(f"{status} id={product_id} | {date.strftime('%d.%m.%Y')} | "
          f"{price} → {result} (ожидалось {expected}) — {comment}")
    return result == expected


def run_extra_tests():
    print("=" * 70)
    print("ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ (5 шт.)")
    print("=" * 70)

    passed = 0
    total = 0

    # Тест 1. Дата расчёта 15.11.2026 → предыдущий месяц = октябрь 2026.
    # В октябре у вас заказов нет → у всех товаров скидка.
    # Товар id=2 (Калифорния, 750) → 750 * 0.75 = 562.5
    total += 1
    passed += check(2, 750.0, datetime(2026, 11, 15), 562.5,
                    "id=2, ноябрь → в октябре заказов нет → скидка")

    # Тест 2. Товар без заказов вообще (id=7, Кола).
    # Дата 15.10.2026 → прошлый месяц сентябрь, у Колы заказов нет → −25%.
    total += 1
    passed += check(7, 100.0, datetime(2026, 10, 15), 75.0,
                    "id=7, без заказов вообще → скидка 25%")

    # Тест 3. Товар с заказом (id=3, Гамбургер).
    # Сентябрь 2026: есть заказ → без скидки.
    total += 1
    passed += check(3, 350.0, datetime(2026, 10, 15), 350.0,
                    "id=3, есть заказ в сентябре → без скидки")

    # Тест 4. Дата расчёта 15.12.2026 → предыдущий месяц = ноябрь 2026.
    # В ноябре заказов нет → скидка всем, включая id=1.
    total += 1
    passed += check(1, 700.0, datetime(2026, 12, 15), 525.0,
                    "id=1, декабрь → в ноябре заказов нет → скидка")

    # Тест 5. Товар id=5 (Болоньезе), 500, дата 15.10.2026.
    # В сентябре у него нет заказов → −25% → 375.
    total += 1
    passed += check(5, 500.0, datetime(2026, 10, 15), 375.0,
                    "id=5, нет заказов в сентябре → скидка")

    print("=" * 70)
    print(f"Пройдено: {passed} / {total}")


if __name__ == "__main__":
    run_extra_tests()