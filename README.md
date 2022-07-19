# Дипломная работа по курсу Python-basic на платформе Skillbox. Telegram-бот по поиску отелей. #

>### Бот осуществляет подбор отелей с сайта [hotels.com](https://ru.hotels.com/) используя открытый [API](https://rapidapi.com/) ###

>#### Имя бота в telegram: @hotels_dip_bot ####
#### Команды для управления ботом: ####
- /help
- /lowprice
- /highprice
- /bestdeal
- /history
 ####Команда /help:  
 Выводит список команд с кратким описанием.
####Команда /lowprice:  
После запроса города для поиска - выводит заданное пользователем количество отелей с <u>наименьшей</u> ценой 
за ночь проживания одного человека.
####Команда /highprice:
После запроса города для поиска - выводит заданное пользователем количество отелей с <u>наибольшей</u> ценой 
за ночь проживания одного человека.
####Команда /bestdeal:
После запроса города для поиска, диапазона цены и расстояния до центра - выводит заданное пользователем количество отелей с <u>наибольшей</u> ценой 
за ночь проживания одного человека.
####Команда /history:  
Выводит историю поиска в виде:  
"Команда"  
"Время и дата запроса"  
"Список отелей"


> Перед запуском бота необходимо установить сторонние модули из файла [requirements.txt](requirements.txt)   
> Затем определить переменные окружения по шаблону [.env.template](.env.template)  
> Запуск бота осуществляется из скрипта [main.py](main.py)
