# =========================
# bot/admin.py
# Admin Panel Features
# =========================

from . import bot
import sqlite3
from telebot.types import ReplyKeyboardMarkup

ADMIN_IDS = [123456789]  # Replace with your Telegram user ID

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "Unauthorized.")
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Add Product", "View Products")
    bot.send_message(message.chat.id, "Admin Panel", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Add Product")
def ask_product_name(message):
    if message.from_user.id not in ADMIN_IDS: return
    msg = bot.send_message(message.chat.id, "Enter product name:")
    bot.register_next_step_handler(msg, get_product_name)

def get_product_name(message):
    bot.user_data = {'name': message.text}
    msg = bot.send_message(message.chat.id, "Enter price:")
    bot.register_next_step_handler(msg, get_product_price)

def get_product_price(message):
    bot.user_data['price'] = int(message.text)
    msg = bot.send_message(message.chat.id, "Enter category:")
    bot.register_next_step_handler(msg, get_product_category)

def get_product_category(message):
    bot.user_data['category'] = message.text
    msg = bot.send_message(message.chat.id, "Enter image URL:")
    bot.register_next_step_handler(msg, save_product)

def save_product(message):
    bot.user_data['image'] = message.text
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, category, image) VALUES (?, ?, ?, ?)",
                (bot.user_data['name'], bot.user_data['price'], bot.user_data['category'], bot.user_data['image']))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "✅ Product added!")

@bot.message_handler(func=lambda m: m.text == "View Products")
def view_products(message):
    if message.from_user.id not in ADMIN_IDS: return
    conn = sqlite3.connect("timo.db")
    cur = conn.cursor()
    cur.execute("SELECT name, price, category FROM products")
    products = cur.fetchall()
    msg = "🗂️ Products:\n"
    for name, price, cat in products:
        msg += f"- {name} ({cat}): {price} KES\n"
    conn.close()
    bot.send_message(message.chat.id, msg)
