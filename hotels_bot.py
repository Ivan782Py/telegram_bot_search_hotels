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


@bot.message_handler(commands=['lowprice'])
def lowprice_print(message):
    msg = bot.send_message(message.chat.id, 'Введите название города')
    bot.register_next_step_handler(msg, search_lowprice)


def search_lowprice(message):
    result = lowprice.search(message.text)
    bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)
