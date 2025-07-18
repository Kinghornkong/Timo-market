bot/__init__.py
# Initializes Bot and Loads Handlers
# ***p****o*****p*****e****+

import os
from telebot import TeleBot
from . import handlers, admin, mpesa

bot = TeleBot(os.environ.get("<add bot api key here!"))
