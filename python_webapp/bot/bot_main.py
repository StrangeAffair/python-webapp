""" Module with bot and token"""

import telebot  # type: ignore # pylint: disable=E0401
from django.conf import settings  # type: ignore # pylint: disable=E0401

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)
