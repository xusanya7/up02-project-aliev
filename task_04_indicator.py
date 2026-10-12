catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2},
]

# Добавляем индикатор
for item in catalog:
    item["status"] = "много" if item["qty"] > 5 else "мало"

# Сортировка: сначала "много", потом "мало"
catalog.sort(key=lambda x: x["status"] != "много")

print("Каталог с индикатором:")
for i, item in enumerate(catalog, start=1):
    print(f"{i}. {item['name']:<10} — {item['qty']} шт. → {item['status']}")
