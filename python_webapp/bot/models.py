"""Module with models"""

from django.db import models  # type: ignore # pylint: disable=E0401


# Create your models here.
class User(models.Model):  # type: ignore # pylint: disable=R0903
    """User module"""
    username = models.CharField(
          verbose_name='Никнейм',
          max_length=20
    )
    external_id = models.PositiveIntegerField(
          verbose_name='telegram user ID',
          unique=True
    )
    reg_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'Пользователь {self.username}'

    class Meta:  # pylint: disable=R0903
        """Name meta class"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class WordRecord(models.Model):  # type: ignore # pylint: disable=R0903
    """Word recording module"""
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0,
    )
    en_word = models.CharField(
        verbose_name='Слово (eng)',
        max_length=50
    )
    ru_translation = models.CharField(
        verbose_name='Перевод (ru)',
        max_length=100
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        default=''
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:  # pylint: disable=R0903
        """Name meta class"""
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'


class LessonRecord(models.Model):  # type: ignore # pylint: disable=R0903
    """Lesson record module"""
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0
    )
    duration = models.IntegerField(
        verbose_name='Длительность'
    )
    date = models.DateTimeField(
        verbose_name='Дата занятия',
        auto_now_add=False
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        default='',
    )

    class Meta:  # pylint: disable=R0903
        """Name meta class"""
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class GameRecord(models.Model):  # type: ignore # pylint: disable=R0903
    """Game record module"""
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0
    )
    date = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True
    )
    n_questions = models.PositiveIntegerField(
        verbose_name='Число вопросов',
    )

    n_answers = models.PositiveIntegerField(
        verbose_name='Число вопросов',
    )

    class Meta:  # pylint: disable=R0903
        """Name meta class"""
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
