import telebot
import main

bot = telebot.TeleBot(main.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user
    user = message.from_user.id
    bot.send_message(user, 'Привет! Я бот по поиску отелей. Введи команду /help')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(user, "Я отвечаю на следующие команды:\n"
                               "/help — помощь по командам бота,\n"
                               "/lowprice — вывод самых дешёвых отелей в городе,\n"
                               "/highprice — вывод самых дорогих отелей в городе,\n"
                               "/bestdeal — вывод отелей, наиболее подходящих по цене и расположению "
                               "от центра.\n "
                               "/history — вывод истории поиска отелей")
    else:
        bot.send_message(user, "Я не понимаю, введите /help")


bot.polling()
