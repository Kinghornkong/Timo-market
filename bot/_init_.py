bot/__init__.py
# Initializes Bot and Loads Handlers
# =========================

import os
from telebot import TeleBot
from . import handlers, admin, mpesa

bot = TeleBot(os.environ.get("7964013672:AAH_8NKlDZQxG590rH9SP30tR65-l687iso"))
