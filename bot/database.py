# =========================
# bot/database.py
# SQLite DB Setup
# =========================

import sqlite3

def init_db():
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        category TEXT,
        image TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS carts (
        user_id INTEGER,
        product_id INTEGER
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT,
        total INTEGER
    )''')
    conn.commit()
    conn.close()
