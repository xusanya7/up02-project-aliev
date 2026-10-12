"""Создаёт таблицы Роль и Пользователь, заполняет тестовыми данными."""

import sqlite3

DB_PATH = "databases/db_variant_15.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Удаляем старые таблицы (если есть)
cur.execute("DROP TABLE IF EXISTS Пользователь")
cur.execute("DROP TABLE IF EXISTS Роль")

# 2. Создаём Роль
cur.execute("""
    CREATE TABLE Роль (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        название TEXT NOT NULL UNIQUE
    )
""")

# 3. Создаём Пользователь с роль_id
cur.execute("""
    CREATE TABLE Пользователь (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        фамилия TEXT NOT NULL,
        имя TEXT NOT NULL,
        отчество TEXT,
        логин TEXT NOT NULL UNIQUE,
        роль_id INTEGER NOT NULL,
        FOREIGN KEY (роль_id) REFERENCES Роль(id)
    )
""")

# 4. Заполняем роли
for name in ("Клиент", "Менеджер", "Администратор"):
    cur.execute("INSERT INTO Роль (название) VALUES (?)", (name,))

# 5. Заполняем пользователей
users = [
    ("Иванов", "Иван", "Иванович", "client1", 1),
    ("Петров", "Петр", "Петрович", "manager1", 2),
    ("Сидоров", "Сидор", "Сидорович", "admin1", 3),
]
for u in users:
    cur.execute(
        "INSERT INTO Пользователь (фамилия, имя, отчество, логин, роль_id) "
        "VALUES (?, ?, ?, ?, ?)",
        u,
    )

conn.commit()

# 6. Показываем результат
print("Роли:")
cur.execute("SELECT * FROM Роль")
for row in cur.fetchall():
    print("  ", row)

print("Пользователи:")
cur.execute("""
    SELECT П.id, П.фамилия, П.имя, П.логин, Р.название
    FROM Пользователь П
    JOIN Роль Р ON П.роль_id = Р.id
""")
for row in cur.fetchall():
    print("  ", row)

conn.close()
print("Готово")
