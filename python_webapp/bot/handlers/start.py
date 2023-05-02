from typing import List, Union

from telebot import types  # type: ignore

from bot.models import User
from bot.bot_main import bot

from bot.utils import start_menu, START_MENU_PREFIX

from bot.handlers.addword import act_on_addword_command
from bot.handlers.addlesson import act_on_addlesson_command
from bot.handlers.game import act_on_game_command
from bot.handlers.stat import act_on_stat_command

from python_webapp.settings import LANGUAGE_CODE

WELCOME_MESSAGE: Union[List[str], str]
WELCOME_BACK_MESSAGE: Union[List[str], str]
if LANGUAGE_CODE.startswith("ru"):
    WELCOME_MESSAGE = [
        "Привет, <b>{user}</b>!",
        "Давай продолжим изучать английский",
    ]
    WELCOME_BACK_MESSAGE = [
        "Привет, <b>{user}</b>, я телеграм-бот",
        "Я могу помочь тебе в изучении английских слов",
        "Пожалуйста, зарегистрируйся через команду /reg",
    ]
else:
    WELCOME_MESSAGE = [
        "Hello, <b>{user}</b>!",
        "Lets continue learning english",
    ]
    WELCOME_BACK_MESSAGE = [
        "Hello, <b>{user}</b>, I am telegram bot",
        "I can help you in remembering new words",
        "Please, registrate via /reg command",
    ]

WELCOME_MESSAGE = '\n'.join(WELCOME_MESSAGE)
WELCOME_BACK_MESSAGE = '\n'.join(WELCOME_BACK_MESSAGE)


def act_on_start_command(message: types.Message) -> None:
    """ Primary handler for /start command"""
    text: Union[List[str], str]

    if User.objects.filter(external_id=message.from_user.id).exists():
        user = User.objects.get(external_id=message.from_user.id)
        """
        text = [
            f"Привет, <b>{user.username}</b>!",
            "Давай продолжим изучать английский",
        ]
        text = ' '.join(text)
        """
        text = WELCOME_BACK_MESSAGE.format(user=user.username)  # type: ignore # noqa: E501
        bot.send_message(
            message.from_user.id,
            text,
            parse_mode='HTML',
            reply_markup=start_menu()
        )

    else:
        """
        text = [
            f"Привет, <b>{message.from_user.username}</b>z я телеграм-бот"
            "Я могу помочь тебе в изучении английских слов",
            "Пожалуйста, зарегистрируйся /reg",
        ]
        text = '\n'.join(text)
        """
        text = WELCOME_MESSAGE.format(user=message.from_user.username)  # type: ignore # noqa: E501
        bot.send_message(
            message.from_user.id,
            text,
            parse_mode='HTML'
        )


def callback_on_start_menu(call: types.CallbackQuery) -> None:
    """ Callback on menu"""
    assert call.data.startswith(START_MENU_PREFIX)

    u_id = call.message.chat.id
    answer = call.data[len(START_MENU_PREFIX):]

    if answer == 'addword':
        act_on_addword_command(u_id)
    elif answer == 'addlesson':
        act_on_addlesson_command(u_id)
    elif answer == 'game':
        act_on_game_command(u_id)
    elif answer == 'stat':
        act_on_stat_command(u_id)
    else:
        bot.send_message(u_id, 'smth wrong')


def register_handler_start() -> None:
    """ Register handlers for /start command"""
    bot.register_message_handler(
        callback=act_on_start_command, commands=['start'])
    bot.register_callback_query_handler(
        callback=callback_on_start_menu,
        func=lambda call: call.data.startswith(START_MENU_PREFIX)
    )
