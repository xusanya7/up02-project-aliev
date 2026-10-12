from config import DB_PATH
import sqlite3

print("DB_PATH =", DB_PATH)

con = sqlite3.connect(DB_PATH)
tables = [
    r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
]
con.close()

print("Таблицы:", tables)
