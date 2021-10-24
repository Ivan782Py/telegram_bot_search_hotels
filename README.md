## Telegram-бот для анализа сайта Hotels.com и поиска подходящих пользователю отелей

>Для получения данных используется открытый [API Hotels](https://rapidapi.com/)

>Имя бота в telegram: @hotels_dip_bot

>Токен для инициализации бота храниться в переменной окружения 'BOT_TOKEN'.

### Структура проекта:
1. _app:
   1. [config.py](_app\config.py) - содержит общие данные.
   2. [functions.py](_app/functions.py) - содержит все функции, необходимые для обработки данных в bot.py.
   3. [req.py](_app/req.py) - содержит все функции для запросов к [API Hotels](https://rapidapi.com/).
2. [bot.py](bot.py) - скрипт для запуска бота.
3. [requirements.txt](requirements.txt) - установка зависимостей. Терминал: pip3 install -r requirements.txt

### Описание:
Бот реагирует на команды:
1. /lowprice: вывод самых дешёвых отелей в городе
2. /highprice: вывод самых дорогих отелей в городе
3. /bestdeal: вывод отелей, наиболее подходящих по цене и расположению от центра
4. /history: вывод истории поиска отелей

После запроса всей необходимой информации от пользователя - бот выводит список отелей (отдельными сообщениями) с учетом всех критериев, заданных пользователем.