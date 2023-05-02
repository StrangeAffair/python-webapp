"""Bot application"""

from django.apps import AppConfig  # type: ignore # pylint: disable=E0401


class BotConfig(AppConfig):  # type: ignore # pylint: disable=R0903
    """Bot application"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
