""" Admin module"""

from django.contrib import admin  # type: ignore # noqa: E501 # pylint: disable=E0401
from .models import WordRecord, LessonRecord, User, GameRecord


# Register your models here.
@admin.register(WordRecord)
class WordRecordAdmin(admin.ModelAdmin):  # type: ignore # noqa: E501 # pylint: disable=R0903
    """word record admin"""
    list_display = ('id', 'en_word', 'ru_translation', 'comment')


@admin.register(LessonRecord)
class LessonRecordAdmin(admin.ModelAdmin):  # type: ignore # noqa: E501 # pylint: disable=R0903
    """lesson record admin"""
    list_display = ('id', 'user', 'duration', 'comment')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore # noqa: E501 # pylint: disable=R0903
    """user admin"""
    list_display = ('id', 'external_id', 'username', 'reg_at')


@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):  # type: ignore # noqa: E501 # pylint: disable=R0903
    """game record admin"""
    list_display = ('id', 'user', 'date', 'n_questions', 'n_answers')
