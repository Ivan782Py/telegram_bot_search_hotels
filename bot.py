import telebot
import re
import os
from dotenv import load_dotenv
from datetime import datetime
from _app import config, functions
from classUsers import Users, User

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=['start', 'help'])
def commands_print(message):
    """ Выводим список команд бота в чат. """
    result = ''
    bot.send_message(message.chat.id, 'Выберите команду:')
    for i_key, i_val in config.command_list.items():
        result += f'{i_key}: {i_val}\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_command(message):
    """ Сохраняем команду.
    Получаем название города. """
    my_time = datetime.now()
    my_time = my_time.strftime('%d-%m-%Y %H:%M')

    user: User = Users.get_user(user_id=message.chat.id)
    user.command.append(message.text)
    user.time.append(my_time)

    msg = bot.send_message(message.chat.id, 'Введите название города:')
    bot.register_next_step_handler(msg, city_search)


@bot.message_handler(commands=['history'])
def search_history(message):
    """ Выводим историю поиска. """
    user: User = Users.get_user(user_id=message.chat.id)
    if user.my_hotels_list:
        for i in range(len(user.command)):
            bot.send_message(message.chat.id, f"Команда: {user.command[i]}\n"
                                              f"Вызвана: {user.time[i]}\n"
                                              f"Список отелей: {user.my_hotels_list[i]}")
    else:
        bot.send_message(message.chat.id, 'Вы еще ничего не искали!')


@bot.message_handler(content_types=['text', 'photo', 'sticker', 'audio'])
def no_answer(message):
    """ Запрашиваем ввод команды от пользователя если он ввел что-то непонятное. """
    bot.send_message(message.chat.id, 'Не понимаю. Введите /help')


def city_search(message):
    """ Проверяем наличие города в базе.
      Получаем количество отелей. """
    city = message.text.lower()
    result = functions.city_check(city_name=city)
    if result:
        user: User = Users.get_user(user_id=message.chat.id)
        user.city_id = result
        msg = bot.send_message(message.chat.id, 'Введите количество отелей, которые необходимо вывести (не более 10):')
        bot.register_next_step_handler(msg, total_hotels)
    else:
        msg = bot.send_message(message.chat.id,
                               f'Не могу найти город {city}, попробуйте изменить название города:')
        bot.register_next_step_handler(msg, city_search)


def total_hotels(message):
    """ Получаем условие по выводу фото. """
    sum_hotels = message.text
    if not sum_hotels.isdigit() or int(sum_hotels) > 10:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 10.\n'
                                                'Попробуйте еще раз:')
        bot.register_next_step_handler(msg, total_hotels)
        return
    else:
        user: User = Users.get_user(user_id=message.chat.id)
        user.sum_hotels = sum_hotels
    msg = bot.send_message(message.chat.id, 'Выводить фото отелей (да/нет)?')
    bot.register_next_step_handler(msg, photo_choice)


def photo_choice(message):
    """ Проверяем ответ по фото.
     Если /bestdeal то запрашиваем диапазон цен. """
    user: User = Users.get_user(user_id=message.chat.id)
    if message.text.lower() == 'да':
        msg = bot.send_message(message.chat.id, 'Сколько фотографий показать (не более 5)?')
        bot.register_next_step_handler(msg, total_photo)
    elif message.text.lower() == 'нет' and user.command[-1] != '/bestdeal':
        bot.send_message(message.chat.id, 'Идет поиск отелей...')
        print_result(message)
    elif user.command[-1] == '/bestdeal':
        msg = bot.send_message(message.chat.id, 'Введите диапазон цен в $, например 30 - 60:')
        bot.register_next_step_handler(msg, set_price)
    else:
        msg = bot.send_message(message.chat.id, 'Я не понимаю. Введите да / нет.')
        bot.register_next_step_handler(msg, photo_choice)


def total_photo(message):
    """ Проверяем ответ по количеству фото.
     Если /bestdeal то запрашиваем диапазон цен. """
    sum_photo = message.text
    user: User = Users.get_user(user_id=message.chat.id)
    user.sum_photo = sum_photo
    if not sum_photo.isdigit() or int(sum_photo) > 5:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 5.\n'
                                                'Попробуйте еще раз.')
        bot.register_next_step_handler(msg, total_photo)
        return
    elif user.command[-1] == '/bestdeal':
        msg = bot.send_message(message.chat.id, 'Введите диапазон цен в $, например 30 - 60:')
        bot.register_next_step_handler(msg, set_price)
    else:
        bot.send_message(message.chat.id, 'Идет поиск отелей...')
        print_result(message)


def set_price(message):
    """ Получаем диапазон цен,
    запрашиваем диапазон расстояния от отеля до центра города. """
    price_list = re.findall(r"\d+", message.text)
    user: User = Users.get_user(user_id=message.chat.id)
    user.price_list = price_list
    if len(price_list) != 2 or not all(i.isdigit() for i in price_list):
        msg = bot.send_message(message.chat.id, 'Так не понимаю, напишите свои числа как в примере:')
        bot.register_next_step_handler(msg, set_price)
        return
    else:
        msg = bot.send_message(message.chat.id, 'Введите диапазон расстояния от отеля до центра '
                                                'в км, например 0.2 - 10:')
        bot.register_next_step_handler(msg, set_distance)


def set_distance(message):
    """ Проверяем введенный диапазон расстояния. """
    dist_list = re.findall(r"[0-9]*[.]?[0-9]+", message.text)
    user: User = Users.get_user(user_id=message.chat.id)
    user.dist_list = dist_list
    if len(dist_list) != 2 or not all(float(i) for i in dist_list):
        msg = bot.send_message(message.chat.id, 'Так не понимаю, напишите свои числа как в примере:')
        bot.register_next_step_handler(msg, set_distance)
        return
    else:
        print_result(message)


def print_result(message):
    """" Выводим результат в чат. """
    user: User = Users.get_user(user_id=message.chat.id)
    result = functions.get_hotels(
        city=user.city_id,
        sum_hotels=user.sum_hotels,
        i_command=user.command[-1],
        choice_price=user.price_list,
        distance=user.dist_list
    )
    hotels_list = list()
    if result:
        for i in range(len(result['id'])):
            name = result['name'][i]
            address = result['address'][i]
            distance = result['distance'][i]
            price = result['price'][i]
            bot.send_message(message.chat.id, f'Название отеля: {name}\n'
                                              f'Адрес: {address}\n'
                                              f'Расстояние до центра: {distance}\n'
                                              f'Цена за сутки: {price} $')
            hotels_list.append(name)
            if user.sum_photo:
                hotel_id = result['id'][i]
                photo_list = functions.get_photo(hotel_id=hotel_id, total=user.sum_photo)
                if photo_list:
                    for photo_url in photo_list:
                        bot.send_photo(message.chat.id, photo=photo_url)
                else:
                    bot.send_sticker(message.chat.id, data=config.my_sticker)
    else:
        bot.send_message(message.chat.id, 'Не удалось ничего найти :(')
    user.my_hotels_list.append(hotels_list)
    return


if __name__ == '__main__':
    bot.polling()
