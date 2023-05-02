from functools import partial

from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import User, WordRecord, LessonRecord

import telebot
from telebot.types import InlineKeyboardButton

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Create your views here.
def index(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('')

@bot.message_handler(commands=['start'])
def act_on_start_command(message):
    string = """Hi, I am a telegram bot!
I can help you study English words.
Please register to continue. /reg
"""
    bot.send_message(message.from_user.id, string)

def get_user_name(message):
    name = message.text
    new_user = User(username=name, external_id=message.from_user.id)
    new_user.save()

    string = f"""Successfully registered user {name}, id={message.from_user.id}.
Now you can use all functions of the bot. \help for more details
"""
    bot.reply_to(message.from_user.id, string)

@bot.message_handler(commands=['reg'])
def act_on_reg_command(message):
    if User.objects.filter(external_id=message.from_user.id).exists():
        bot.send_message(
             message.from_user.id,
             "You are already registered :)"
        )
    else:
        bot.send_message(
            message.from_user.id,
            "Let's start the registration! What is your name?"
        )
        bot.register_next_step_handler(message, callback=get_user_name)

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['addword'])
def act_on_addword_command(message):
    if not User.objects.filter(external_id=message.from_user.id):
        bot.send_message(
             message.from_user.id,
             "Please, register first. \\reg"
        )
        return

    user = User.objects.get(external_id=message.from_user.id)
    bot.send_message(
        message.from_user.id,
        "Enter new word or expression: "
    )
    word_record = WordRecord(user=user)

    bot.register_next_step_handler(message, callback=partial(get_word_record_en_word, word_record))

def get_word_record_en_word(word_record: WordRecord, message):
    word_record.en_word = message.text

    bot.send_message(
        message.from_user.id,
        f"Fine, {message.text} is writen. Enter translation."
    )
    bot.register_next_step_handler(message, word_record, callback=get_word_record_ru_translation)

def get_word_record_ru_translation(message, word_record: WordRecord):
    word_record.ru_translation = message.text

    bot.send_message(
        message.from_user.id,
        f"Fine, {message.text} is tranlation. Any comments?"
    )
    bot.register_next_step_handler(message, word_record, callback=get_word_record_ru_translation)

def get_word_record_comment(message, word_record: WordRecord):
    word_record.comment = message.text

    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text='Yes', callback_data='yes'),
        InlineKeyboardButton(text='No', callback_data='no')
    )

    text = f"Got it. Is everything alright?\
           {word_record.en_word} = {word_record.ru_translation} ({word_record.comment})"

    bot.send_message(message.from_user.id, text=text, reply_markup=kb)

    bot.register_next_step_handler(message, word_record, callback=word_record_confirm)

def word_record_confirm(message, word_record: WordRecord):

    if message.text == 'yes':
        word_record.save()
        text = f"Great! {word_record.en_word} is added to your dictionary."
    elif message.text == 'no':
        text = f"Sorry... Let's try again."

    bot.send_message(message.from_user.id, text=text)

bot.polling(non_stop=True)
