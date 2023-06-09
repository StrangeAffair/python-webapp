"""Views file"""

# from functools import partial

# from django.shortcuts import render  # type: ignore
# from django.conf import settings  # type: ignore
# from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest  # type: ignore # noqa: E501 # pylint: disable=E0401
# from .models import User, WordRecord, LessonRecord

import telebot  # type: ignore # pylint: disable=E0401
# from telebot.types import InlineKeyboardButton

from bot.bot_main import bot
from bot.handlers import reg, start, addword, addlesson, stat, delete
from bot.handlers import help as help_cmd


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """Handle request"""
    if request.META['CONTENT_TYPE'] == 'application/json':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('')


reg.register_handler_reg()
start.register_handler_start()
addword.register_handler_addword()
addlesson.register_handler_addlesson()
stat.register_stat_handler()
delete.register_del_handler()
help_cmd.register_help_handler()

bot.polling(non_stop=True)
