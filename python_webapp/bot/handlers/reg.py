from typing import List, Union

from bot.bot_main import bot
from bot.models import User
from telebot import types  # type: ignore

from bot.utils import start_menu, START_TEXT


def act_on_reg_command(message: types.Message) -> None:
    """ Primary handler to /reg command"""

    if User.objects.filter(external_id=message.from_user.id).exists():
        user = User.objects.get(external_id=message.from_user.id)

        bot.send_message(
            message.from_user.id,
            (f"<b>{user.username}</b>, вы уже зарегистрированы\n"
             "Для удаления профиля используйте /del"),
            parse_mode='HTML'
        )
    else:
        msg = bot.send_message(
            message.from_user.id,
            "Начнем регистрацию. Как вас зовут?"
        )
        bot.register_next_step_handler(msg, callback=get_user_name)


def get_user_name(message: types.Message) -> None:
    """ Handler to get user name """
    text: Union[List[str], str]

    name = message.text
    new_user = User(username=name, external_id=message.from_user.id)
    new_user.save()

    text = [
        f"Добро пожаловать, <b>{name}</b>",
        "Теперь ты можешь использовать все функции бота",
        "Для справки используй /help",
    ]
    text = '\n'.join(text)
    bot.reply_to(message, text, parse_mode='HTML')

    u_id = message.chat.id
    bot.send_message(u_id, text=START_TEXT, parse_mode='HTML',
                     reply_markup=start_menu())


def register_handler_reg() -> None:
    """ Register handler for /reg command """
    bot.register_message_handler(commands=['reg'], callback=act_on_reg_command)
