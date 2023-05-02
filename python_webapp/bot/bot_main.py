import telebot  # type: ignore
from django.conf import settings  # type: ignore
from telebot.types import InlineKeyboardButton  # type: ignore

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)
