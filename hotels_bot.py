import telebot
import lowprice

TOKEN = "1924202795:AAERxHoCbjim_Y0mg_klbVTMXmMQWWp3N1I"
bot = telebot.TeleBot(TOKEN)

commands = {
    '/lowprice': 'вывод самых дешёвых отелей в городе',
    '/highprice': 'вывод самых дорогих отелей в городе',
    '/bestdeal': 'вывод отелей, наиболее подходящих по цене и расположению от центра',
    '/history': 'вывод истории поиска отелей'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я бот по поиску отелей. '
                                      'Введите команду /help чтобы увидеть что я могу.')


@bot.message_handler(commands=['help'])
def commands_print(message):
    result = ''
    for i_key, i_val in commands.items():
        result += f'{i_key}: {i_val}\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_command(message):
    global i_command
    i_command = message.text
    msg = bot.send_message(message.chat.id, 'Введите название города на англ. языке (пример: new york')
    bot.register_next_step_handler(msg, search_city)


def search_city(message):
    global city
    city = message.text.lower()
    msg = bot.send_message(message.chat.id, 'Введите количество отелей, которые необходимо вывести (не более 20)')
    bot.register_next_step_handler(msg, total_hotels)


def total_hotels(message):
    global sum_hotels
    sum_hotels = message.text
    if not sum_hotels.isdigit() or int(sum_hotels) > 20:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 20. Попробуйте еще раз.')
        bot.register_next_step_handler(msg, total_hotels)
        return
    msg = bot.send_message(message.chat.id, 'Выводить фото отелей (да/нет)?')
    bot.register_next_step_handler(msg, photo_choice)


def photo_choice(message):
    global i_photo
    i_photo = False
    if message.text.lower() == 'да':
        i_photo = True
        msg = bot.send_message(message.chat.id, 'Сколько фотографий показать (не более 5)?')
        bot.register_next_step_handler(msg, total_photo)


def total_photo(message):
    global sum_photo
    sum_photo = message.text
    if not sum_photo.isdigit() or int(sum_photo) > 5:
        msg = bot.send_message(message.chat.id, 'Ответом должно быть число, не более 5. Попробуйте еще раз.')
        bot.register_next_step_handler(msg, total_photo)
        return
    bot.send_message(message.chat.id, f'Вывожу результат поиска по команде {i_command}, напишите Ок.')
    # Это откровенный костыль. Не могу придумать как перейти к search_hotels() без получения сообщения от пользователя.
    bot.register_next_step_handler(message, search_hotels)


def search_hotels(message):
    if i_command == '/lowprice':
        result = lowprice.search(i_city=city, total=sum_hotels, photo=sum_photo)
    else:
        result = 'Пока не знаю такой команды'
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
