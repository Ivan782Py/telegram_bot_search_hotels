import telebot
from datetime import datetime
from _app import config, functions

bot = telebot.TeleBot(config.TOKEN)

history_dict = {'command': [], 'time': [], 'hotels': []}


@bot.message_handler(commands=['start', 'help'])
def commands_print(message):
    """ Выводим список команд бота в чат """
    result = ''
    bot.send_message(message.chat.id, 'Привет! Я бот по поиску отелей. '
                                      'Я могу выполнить команды:')
    for i_key, i_val in config.command_list.items():
        result += f'{i_key}: {i_val}\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_command(message):
    """ Получаем название города, сохраняем команду """
    global i_command
    i_command = message.text

    my_time = datetime.now()
    my_time = my_time.strftime('%d-%m-%Y %H:%M')
    history_dict['command'].append(i_command)
    history_dict['time'].append(my_time)

    msg = bot.send_message(message.chat.id, 'Введите название города на английском языке (пример: new york)')
    bot.register_next_step_handler(msg, city_search)


@bot.message_handler(commands=['history'])
def my_history(message):
    """ Выводим историю поиска """
    for i in range(len(history_dict['command'])):
        i_com = history_dict['command'][i]
        i_time = history_dict['time'][i]
        i_hotels_list = history_dict['hotels'][i]

        bot.send_message(message.chat.id, f"Команда: {i_com}\n"
                                          f"Вызвана: {i_time}\n"
                                          f"Список отелей: {i_hotels_list}")


@bot.message_handler(content_types=['text', 'photo', 'sticker', 'audio'])
def no_answer(message):
    """ Запрашиваем ввод команды от пользователя если он что-то ввел другое """
    bot.send_message(message.chat.id, 'Не понимаю. Введите /help')


def city_search(message):
    """ Проверяем наличие города в базе
      Получаем количество отелей """
    global city
    city = message.text.lower()
    result: bool = functions.city_check(city_name=city)
    if result:
        msg = bot.send_message(message.chat.id, 'Введите количество отелей, которые необходимо вывести (не более 10)')
        bot.register_next_step_handler(msg, total_hotels)
    else:
        msg = bot.send_message(message.chat.id,
                               f'Не могу найти город {city}, попробуйте изменить название (пример: new york)')
        bot.register_next_step_handler(msg, city_search)


def total_hotels(message):
    """ Получаем условие по выводу фото """
    global sum_hotels
    sum_hotels = message.text
    if not sum_hotels.isdigit() or int(sum_hotels) > 10:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 10.\n'
                                                'Попробуйте еще раз.')
        bot.register_next_step_handler(msg, total_hotels)
        return
    msg = bot.send_message(message.chat.id, 'Выводить фото отелей (да/нет)?')
    bot.register_next_step_handler(msg, photo_choice)


def photo_choice(message):
    """ Проверяем ответ по фото.
    Если /bestdeal то запрашиваем диапазон цен"""
    if message.text.lower() == 'да':
        msg = bot.send_message(message.chat.id, 'Сколько фотографий показать (не более 5)?')
        bot.register_next_step_handler(msg, total_photo)
    elif message.text.lower() == 'нет' and i_command != '/bestdeal':
        print_result(message)
    elif i_command == '/bestdeal':
        msg = bot.send_message(message.chat.id, 'Введите диапазон цен в $, например 30 - 60:')
        bot.register_next_step_handler(msg, set_price)
    else:
        msg = bot.send_message(message.chat.id, 'Я не понимаю. Введите да / нет.')
        bot.register_next_step_handler(msg, photo_choice)


sum_photo = None


def total_photo(message):
    """ Проверяем ответ по количеству фото
    Если /bestdeal то запрашиваем диапазон цен"""
    global sum_photo
    sum_photo = message.text
    if not sum_photo.isdigit() or int(sum_photo) > 5:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 5.\n'
                                                'Попробуйте еще раз.')
        bot.register_next_step_handler(msg, total_photo)
        return
    elif i_command == '/bestdeal':
        msg = bot.send_message(message.chat.id, 'Введите диапазон цен в $, например 30 - 60:')
        bot.register_next_step_handler(msg, set_price)
    else:
        print_result(message)


price_list = None


def set_price(message):
    """ Получаем диапазон расстояния от отеля до центра города """
    global price_list
    price_list = message.text.split('-')
    price_list = [x.strip() for x in price_list]
    if len(price_list) != 2 or not all(i.isdigit() for i in price_list):
        msg = bot.send_message(message.chat.id, 'Так не понимаю, напишите свои числа как в примере:')
        bot.register_next_step_handler(msg, set_price)
        return
    else:
        msg = bot.send_message(message.chat.id, 'Введите диапазон расстояния от отеля до центра '
                                                'в милях, например 0.7 - 10:')
        bot.register_next_step_handler(msg, set_distance)


dist_list = None


def set_distance(message):
    """ Проверяем введенный диапазон расстояния """
    global dist_list
    dist_list = message.text.split('-')
    dist_list = [x.strip() for x in dist_list]
    if len(dist_list) != 2 or not all(float(i) for i in dist_list):
        msg = bot.send_message(message.chat.id, 'Так не понимаю, напишите свои числа как в примере:')
        bot.register_next_step_handler(msg, set_distance)
        return
    else:
        print_result(message)


def print_result(message):
    """" Выводим результат в чат """
    my_dict = functions.get_hotels(city=city, num_hotels=sum_hotels, i_command=i_command,
                                   choice_price=price_list, distance=dist_list
                                   )

    hotels_list = []
    if my_dict:
        for i in range(len(my_dict['id'])):
            name = my_dict['name'][i]
            address = my_dict['address'][i]
            distance = my_dict['distance'][i]
            price = my_dict['price'][i]
            bot.send_message(message.chat.id, f'Название отеля: {name}\n'
                                              f'Адрес: {address}\n'
                                              f'Расстояние до центра: {distance}\n'
                                              f'Цена за сутки: {price} $')
            hotels_list.append(name)

            if sum_photo:
                hotel_id = my_dict['id'][i]
                photo_list = functions.get_photo(hotel_id=hotel_id, total=sum_photo)
                if photo_list:
                    for photo_url in photo_list:
                        bot.send_photo(message.chat.id, photo=photo_url)
                else:
                    bot.send_sticker(message.chat.id, send_sticker=config.my_stiker)
    else:
        bot.send_message(message.chat.id, 'Не удалось ничего найти :(')
        hotels_list.append('Пусто.')
    history_dict['hotels'].append(hotels_list)
    return


if __name__ == '__main__':
    bot.polling(non_stop=True)
