# =========================
# bot/handlers.py
# Bot Commands and Callback Handlers
# =========================

from . import bot
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to TIMO 🛍️!\nUse /shop to browse products.")

@bot.message_handler(commands=['shop'])
def show_products(message):
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products")
    rows = cur.fetchall()
    for pid, name, price in rows:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Add to cart", callback_data=f"add_{pid}"))
        bot.send_message(message.chat.id, f"{name} - {price} KES", reply_markup=markup)
    conn.close()

@bot.message_handler(commands=['cart'])
def show_cart(message):
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute('''SELECT p.name, p.price FROM carts c JOIN products p ON c.product_id = p.id WHERE c.user_id=?''', (message.chat.id,))
    items = cur.fetchall()
    if not items:
        bot.reply_to(message, "🛒 Your cart is empty.")
    else:
        msg = "🛒 Your cart:\n"
        total = 0
        for name, price in items:
            msg += f"- {name}: {price} KES\n"
            total += price
        msg += f"\nTotal: {total} KES"
        bot.reply_to(message, msg)
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart(call):
    product_id = int(call.data.split("_")[1])
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO carts (user_id, product_id) VALUES (?, ?)", (call.from_user.id, product_id))
    conn.commit()
    conn.close()
    bot.answer_callback_query(call.id, "✅ Added to cart")
