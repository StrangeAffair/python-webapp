"""Validators, common keyboards"""

from datetime import datetime
from telebot import types  # type: ignore # pylint: disable=E0401

from python_webapp.settings import LANGUAGE_CODE

BUTTON_ADDWORD_TEXT: str
BUTTON_ADDLESSON_TEXT: str
BUTTON_REPEAT_TEXT: str
BUTTON_STAT_TEXT: str
if LANGUAGE_CODE.startswith("ru"):
    BUTTON_ADDWORD_TEXT = "Добавить новое слово"
    BUTTON_ADDLESSON_TEXT = "Записать урок"
    BUTTON_REPEAT_TEXT = "Повторять слова"
    BUTTON_STAT_TEXT = "Статистика"
else:
    BUTTON_ADDWORD_TEXT = "Add new word"
    BUTTON_ADDLESSON_TEXT = "Add new lesson"
    BUTTON_REPEAT_TEXT = "Repeat words"
    BUTTON_STAT_TEXT = "Statistics"


def date_validator(data_text: str) -> bool:
    """validate date"""
    try:
        datetime.strptime(data_text, '%d.%m.%Y')
    except ValueError:
        return False

    return True


def date_str_to_django(data_text: str) -> str:
    """Convert str to django str"""
    assert date_validator(data_text)
    date = datetime.strptime(data_text, '%d.%m.%Y')

    return date.strftime('%Y-%m-%d %H:%M')


def date_django_to_str(date: str) -> str:
    """Convert django str to user str"""
    return datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d-%m-%Y')


def int_validator(text: str) -> bool:
    """ Validate int number"""
    return text.isdecimal() and (int(text) < 24*60)


def word_validator(text: str) -> bool:
    """ Validate word"""
    return text.isalnum() and (len(text) < 100)


def get_yes_no_inline_keyboard(prefix: str, yes_text: str, no_text: str
                               ) -> types.ReplyKeyboardMarkup:
    """ Keyboard creator"""
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        types.InlineKeyboardButton(
            text=yes_text,
            callback_data=prefix + 'yes'
        ),
        types.InlineKeyboardButton(
            text=no_text,
            callback_data=prefix + 'no'
        )
    )

    return ikbm


START_MENU_PREFIX = "start_menu_keyboard_"
if LANGUAGE_CODE.startswith("ru"):
    START_TEXT = "Давай продолжим изучать английский 🧠"
else:
    START_TEXT = "Lets continue study english"


def start_menu() -> types.InlineKeyboardMarkup:
    """Start menu keyboard"""
    ikbm = types.InlineKeyboardMarkup(row_width=1)

    ikbm.add(
        types.InlineKeyboardButton(
            text=BUTTON_ADDWORD_TEXT,
            callback_data=START_MENU_PREFIX + 'addword'
        ),
        types.InlineKeyboardButton(
            text=BUTTON_ADDLESSON_TEXT,
            callback_data=START_MENU_PREFIX + 'addlesson'
        ),
        types.InlineKeyboardButton(
            text=BUTTON_REPEAT_TEXT,
            callback_data=START_MENU_PREFIX + 'game'
        ),
        types.InlineKeyboardButton(
            text=BUTTON_STAT_TEXT,
            callback_data=START_MENU_PREFIX + 'stat'
        )
    )

    return ikbm
