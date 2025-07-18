
# =========================
# app.py
# Main Flask App and Bot Launcher
# =========================

from flask import Flask, request
from telebot.types import Update
from dotenv import load_dotenv
import os
from bot import bot, init_db

load_dotenv()
app = Flask(__name__)

init_db()

@app.route(f"/{os.environ.get('TELEGRAM_API_TOKEN')}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def home():
    return "TIMO Telegram Bot is Live!"

if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
