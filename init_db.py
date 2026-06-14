import sqlite3

db = sqlite3.connect("database.db")

with open("schema.sql", encoding="utf-8") as f:
    db.executescript(f.read())

with open("init.sql", encoding="utf-8") as f:
    db.executescript(f.read())

db.close()

print("Tietokanta luotu.")