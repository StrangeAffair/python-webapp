from typing import List, Union

from telebot import types  # type: ignore
from typing import Dict

from bot.bot_main import bot
from bot.models import User, WordRecord
from bot.utils import get_yes_no_inline_keyboard, start_menu
from bot.utils import word_validator

from python_webapp.settings import LANGUAGE_CODE

# prefixes to distinguish between callback queris
comment_prefix = 'comment_addword_inline_keyboard_'
confirm_prefix = 'confirm_addword_inline_keyabord_'

# to store data before saving in db
g_input_user_data: Dict[int, WordRecord] = {}

ADDWORD_ENWORD_TEXT: str
ADDWORD_RUWORD_TEXT: str
ADDWORD_COMMENT_TEXT: str
ADDWORD_ADDCOMMENT_TEXT: str
ADDWORD_NOCOMMENT_TEXT: str
ADDWORD_CONFIRM_TEXT_LIST: List[str]
ADDWORD_CONFIRM_TEXT: str
ADDWORD_DICTADD_TEXT_LIST: List[str]
ADDWORD_DICTADD_TEXT: str
ADDWORD_YES: str
ADDWORD_NO: str
if LANGUAGE_CODE.startswith("ru"):
    ADDWORD_ENWORD_TEXT = "Введите новое слово:"
    ADDWORD_RUWORD_TEXT = "Записано <i>{word}</i>. Введите перевод:"
    ADDWORD_COMMENT_TEXT = "Перевод записан <i>{word}</i>. Добавить пояснение?"
    ADDWORD_ADDCOMMENT_TEXT = "Введите пояснение"
    ADDWORD_NOCOMMENT_TEXT = "Пояснение отсутствует"
    ADDWORD_CONFIRM_TEXT_LIST = [
        "Все правильно?",
        "Слово: <i>{en_word}</i>",
        "Перевод: <i>{ru_word}</i>",
        "Комментарий: <i>{comment}</i>",
    ]
    ADDWORD_CONFIRM_TEXT = '\n'.join(ADDWORD_CONFIRM_TEXT_LIST)
    ADDWORD_DICTADD_TEXT_LIST = [
        "Cлово",
        "<i>{word}</i>",
        "успешно добавлено в словарь",
    ]
    ADDWORD_DICTADD_TEXT = ' '.join(ADDWORD_DICTADD_TEXT_LIST)
    ADDWORD_YES = "Да"
    ADDWORD_NO = "Нет"
else:
    ADDWORD_ENWORD_TEXT = "Enter new word:"
    ADDWORD_RUWORD_TEXT = "Written down word <i>{word}</i>. Enter translation:"
    ADDWORD_COMMENT_TEXT = "Written down translation <i>{word}</i>. Comment?"
    ADDWORD_ADDCOMMENT_TEXT = "Enter comment"
    ADDWORD_NOCOMMENT_TEXT = "No comment"
    ADDWORD_CONFIRM_TEXT_LIST = [
        "All is right?",
        "Word: <i>{en_word}</i>",
        "Translation: <i>{ru_word}</i>",
        "Comment: <i>{comment}</i>",
    ]
    ADDWORD_CONFIRM_TEXT = '\n'.join(ADDWORD_CONFIRM_TEXT_LIST)
    ADDWORD_DICTADD_TEXT_LIST = [
        "Word",
        "<i>{word}</i>",
        "was added to dictonary",
    ]
    ADDWORD_DICTADD_TEXT = ' '.join(ADDWORD_DICTADD_TEXT_LIST)
    ADDWORD_YES = "Yes"
    ADDWORD_NO = "No"


def act_on_addword_command(u_id: int) -> None:
    """ Handler to addword command"""

    user = User.objects.get(external_id=u_id)

    text = ADDWORD_ENWORD_TEXT
    msg = bot.send_message(u_id, text=text)

    global g_input_user_data
    g_input_user_data[u_id] = WordRecord(user=user)

    bot.register_next_step_handler(
        msg,
        callback=get_word_record_en_word
    )


def get_word_record_en_word(message: types.Message) -> None:
    """ Get enlish word from message"""
    text: Union[List[str], str]

    u_id = message.from_user.id
    user = User.objects.get(external_id=u_id)
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    entered_data = message.text
    # validation of entered data
    if not word_validator(entered_data):
        text = [
            f"Неправильный формат (<b>{entered_data}</b>)",
            "Слово может содержать только буквы и цифры.",
            "Введите слово ещё раз:",
        ]
        text = '\n'.join(text)

        msg = bot.send_message(u_id, text=text, parse_mode='HTML')
        bot.register_next_step_handler(msg, callback=get_word_record_en_word)
        return

    g_input_user_data[u_id].en_word = message.text.lower()

    word = message.text.lower()
    if WordRecord.objects.filter(user=user, en_word=word).exists():
        word = WordRecord.objects.get(user=user, en_word=word)
        text = [
            "Такое слово уже есть в словаре",
            f"Слово: <i>{word.en_word}</i>",
            f"Перевод: <i>{word.ru_translation}</i>",
            f"[<i>{word.comment}</i>]",
        ]
        text = '\n'.join(text)

        print(text)
        bot.send_message(u_id, text=text, parse_mode='HTML',
                         reply_markup=start_menu())
        return

    text = ADDWORD_RUWORD_TEXT.format(word=message.text)

    bot.send_message(u_id, text=text, parse_mode='HTML')

    bot.register_next_step_handler(
        message,
        callback=get_word_record_ru_translation
    )


def get_word_record_ru_translation(message: types.Message) -> None:
    """ Get translation from message """
    text: Union[List[str], str]

    u_id = message.from_user.id
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    entered_data = message.text
    # validation of entered data
    if not word_validator(entered_data):
        text = [
            f"Неправильный формат (<b>{entered_data}</b>)",
            "Слово может содержать только буквы и цифры.",
            "Введите слово ещё раз:",
        ]
        text = '\n'.join(text)

        msg = bot.send_message(u_id, text=text, parse_mode='HTML')

        callback = get_word_record_ru_translation
        bot.register_next_step_handler(msg, callback=callback)
        return

    g_input_user_data[u_id].ru_translation = message.text

    text = ADDWORD_COMMENT_TEXT.format(word=message.text)

    yes_text = ADDWORD_YES
    no_text = ADDWORD_NO
    kb = get_yes_no_inline_keyboard(comment_prefix, yes_text, no_text)

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_comment(call: types.CallbackQuery) -> None:
    """ Callback on question about comment"""
    assert call.data.startswith(comment_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(comment_prefix):]

    if answer == 'yes':
        msg = bot.send_message(u_id, text=ADDWORD_ADDCOMMENT_TEXT)
        bot.register_next_step_handler(msg, callback=get_word_record_comment)
    elif answer == 'no':
        msg = bot.send_message(u_id, text=ADDWORD_NOCOMMENT_TEXT)
        confirm_add_word(u_id)


def get_word_record_comment(message: types.Message) -> None:
    """ Get comment from the message"""
    u_id = message.from_user.id
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    g_input_user_data[u_id].comment = message.text

    confirm_add_word(u_id)


def confirm_add_word(u_id: int) -> None:
    """ Show confirm keyboard"""
    global g_input_user_data
    if not (u_id in g_input_user_data):
        return

    word = g_input_user_data[u_id]

    comment = f"\n({word.comment})" if word.comment != '' else ''
    text = ADDWORD_CONFIRM_TEXT.format(
        en_word=word.en_word,
        ru_word=word.ru_translation,
        comment=comment
    )

    yes_text = ADDWORD_YES
    no_text = ADDWORD_NO
    kb = get_yes_no_inline_keyboard(confirm_prefix, yes_text, no_text)

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_cofirm_add_word(call: types.CallbackQuery) -> None:
    """ Callback on confirmation question"""
    text: Union[List[str], str]

    assert call.data.startswith(confirm_prefix)
    global g_input_user_data

    u_id = call.message.chat.id
    answer = call.data[len(confirm_prefix):]

    if not (u_id in g_input_user_data):
        return

    if answer == 'yes':
        g_input_user_data[u_id].save()
        text = ADDWORD_DICTADD_TEXT.format(
            word=g_input_user_data[u_id].en_word
        )

    elif answer == 'no':
        text = "Упс... Давайте попробуем еще раз"

    # remove tmp input data
    g_input_user_data.pop(u_id)

    bot.send_message(u_id, text=text, parse_mode='HTML',
                     reply_markup=start_menu())


def register_handler_addword() -> None:
    """ register handlers for addword command"""
    bot.register_callback_query_handler(
        callback=callback_on_cofirm_add_word,
        func=lambda call: call.data.startswith(confirm_prefix)
    )
    bot.register_callback_query_handler(
        callback=callback_on_comment,
        func=lambda call: call.data.startswith(comment_prefix)
    )
