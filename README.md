# python-webapp

Телеграм бот-словарь.

## Команды:
1. /start -- начать работу с ботом
2. /reg -- регистрация
3. /del -- удаление
4. /help -- помощь
5. /stat -- статистика
6. /addword -- добавить слово

## Запуск:
1. git clone https://github.com/StrangeAffair/python-webapp.git
2. python3 -m pip install -r requirement.txt
3. Создать файл .env, в котором записать
    * DJANGO_SECRET_KEY = 'ваш секретный ключ'
    * TELEGRAM_BOT_TOKEN = 'ваш токен для бота'
4. python3 manage.py runserver
