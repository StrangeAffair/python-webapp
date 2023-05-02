from django.shortcuts import render

from django.conf import settings

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

import telebot


TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Create your views here.
def index(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, '<b>message.text</b>', parse_mode='HTML')

bot.polling(non_stop=True)

