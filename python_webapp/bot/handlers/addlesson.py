"""Module for adding lessons"""

from typing import List, Union

from telebot import types  # type: ignore
from typing import Dict

from bot.bot_main import bot
from bot.models import User, LessonRecord

from bot.utils import date_validator, date_str_to_django, date_django_to_str
from bot.utils import get_yes_no_inline_keyboard, start_menu
from bot.utils import int_validator

# prefixes for queries handlers
COMMENT_PREFIX = 'comment_addlesson_inline_keyboard_'
CONFIRM_PREFIX = 'confirm_addlesson_inline_keyabord_'

# to store temporary data before saving in db
g_input_user_data: Dict[int, LessonRecord] = {}


def act_on_addlesson_command(u_id: int) -> None:
    """Handler for addlesson command"""

    user = User.objects.get(external_id=u_id)
    text = "Введите дату урока в формате дд.мм.гггг:"
    msg = bot.send_message(u_id, text=text)

    g_input_user_data[u_id] = LessonRecord(user=user)

    bot.register_next_step_handler(msg, callback=get_date)


def get_date(message: types.Message) -> None:
    """ Get date from the message"""
    u_id = message.from_user.id

    if u_id not in g_input_user_data:
        return

    entered_date = message.text

    # validation of entered data
    if not date_validator(entered_date):
        text = (f"Неправильный формат даты (<b>{entered_date}</b>)"
                "Должно быть <u>дд.мм.гггг</u>"
                "Введите еще раз:")

        msg = bot.send_message(u_id, text=text, parse_mode='HTML')
        bot.register_next_step_handler(msg, callback=get_date)
        return

    text = f"""Записал <i>{entered_date}</i>
Введите длительность урока в минутах:
"""
    bot.send_message(u_id, text=text, parse_mode='HTML')

    g_input_user_data[u_id].date = date_str_to_django(entered_date)

    bot.register_next_step_handler(message, callback=get_duration)


def get_duration(message: types.Message) -> None:
    """ Get duration from the message"""
    text: Union[List[str], str]

    u_id = message.from_user.id

    if u_id not in g_input_user_data:
        return

    entered_data = message.text

    if not int_validator(entered_data):
        text = (f"""Неправильный формат числа (<b>{entered_data}</b>)
Давайте еще раз:""")
        msg = bot.send_message(u_id, text=text, parse_mode='HTML')
        bot.register_next_step_handler(msg, callback=get_duration)
        return

    g_input_user_data[u_id].duration = int(message.text)

    yes_text = 'Да'
    no_text = 'Нет'
    kb = get_yes_no_inline_keyboard(COMMENT_PREFIX, yes_text, no_text)

    text = [
        f"Отлично, записал <i>{message.text}</i> (минуты)",
        "Добавить пояснение?",
    ]
    text = "".join(text)
    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_comment(call: types.CallbackQuery) -> None:
    """ Callback on question about comment """
    assert call.data.startswith(COMMENT_PREFIX)

    u_id = call.message.chat.id
    answer = call.data[len(COMMENT_PREFIX):]

    if u_id not in g_input_user_data:
        return

    if answer == 'yes':
        msg = bot.send_message(u_id, text="Введите пояснение")
        bot.register_next_step_handler(msg, callback=get_lesson_record_comment)

    elif answer == 'no':
        g_input_user_data[u_id].comment = ''
        msg = bot.send_message(u_id, text="Пояснение отсутствует")

        confirm_add_lesson(u_id)
    else:
        bot.send_message(u_id, text='smth wrong')


def get_lesson_record_comment(message: types.Message) -> None:
    """ Get comment from the message """
    u_id = message.from_user.id

    if u_id not in g_input_user_data:
        return

    g_input_user_data[u_id].comment = message.text
    confirm_add_lesson(u_id)


def confirm_add_lesson(u_id: int) -> None:
    """ Show confirm keyboard"""
    global g_input_user_data

    if u_id not in g_input_user_data:
        return

    lesson = g_input_user_data[u_id]
    comment = f"\n({lesson.comment})" if lesson.comment != '' else ''
    text = (f"Все верно?\n"
            f"Дата: <i>{date_django_to_str(lesson.date)}</i>\n"
            f"Длительность: <i>{lesson.duration}</i>" +
            comment)

    yes_text = "Да"
    no_text = "Нет"
    kb = get_yes_no_inline_keyboard(CONFIRM_PREFIX, yes_text, no_text)

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_cofirm_add_lesson(call: types.CallbackQuery) -> None:
    """ Callback on confirmation"""
    assert call.data.startswith(CONFIRM_PREFIX)
    global g_input_user_data

    u_id = call.message.chat.id
    answer = call.data[len(CONFIRM_PREFIX):]

    if u_id not in g_input_user_data:
        return

    if answer == 'yes':
        g_input_user_data[u_id].save()
        text = "Урок успешно записан"
    elif answer == 'no':
        text = "Упс... Давайте попробуем еще раз"

    # remove tmp input data
    g_input_user_data.pop(u_id)

    bot.send_message(u_id, text=text, parse_mode='HTML',
                     reply_markup=start_menu())


def register_handler_addlesson() -> None:
    """ Register handlers for addlesson command"""
    bot.register_callback_query_handler(
        callback=callback_on_cofirm_add_lesson,
        func=lambda call: call.data.startswith(CONFIRM_PREFIX)
    )
    bot.register_callback_query_handler(
        callback=callback_on_comment,
        func=lambda call: call.data.startswith(COMMENT_PREFIX)
    )
