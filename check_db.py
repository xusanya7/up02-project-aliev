from config import DB_PATH
import sqlite3

print("DB_PATH =", DB_PATH)

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("Таблицы в БД:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(" -", row[0])

print("\nСхема (первые строки):")
for row in cur.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
    print(row[0], "\n")

con.close()