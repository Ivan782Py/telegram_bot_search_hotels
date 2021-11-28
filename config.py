import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("API_TOKEN")
}

command_list = {
    '/lowprice': 'вывод самых дешёвых отелей в городе',
    '/highprice': 'вывод самых дорогих отелей в городе',
    '/bestdeal': 'вывод отелей, наиболее подходящих по цене и расположению от центра',
    '/history': 'вывод истории поиска отелей'
}

my_sticker = 'CAACAgIAAxkBAAIDRWFoPEAB37gKiyC9y6US7W3dNYT3AAJHAwACbbBCA1JVK_k1xYCCIQQ'
