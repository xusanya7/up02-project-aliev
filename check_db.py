"""Проверка структуры БД."""
import sqlite3
from pathlib import Path

# Найдём файл БД в папке databases/
db_dir = Path("databases")
for f in db_dir.glob("*.db"):
    print(f"\n=== Файл: {f} ===")
    con = sqlite3.connect(f)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print("Таблицы:", tables)

    for (tbl,) in tables:
        cur.execute(f"PRAGMA table_info({tbl})")
        cols = cur.fetchall()
        print(f"\nТаблица '{tbl}' — колонки:")
        for c in cols:
            print(f"  {c[1]} ({c[2]})")
    con.close()