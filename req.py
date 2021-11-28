import requests
import json
import config
from loguru import logger
from datetime import datetime, timedelta
from typing import Optional


logger.add("errors.log")


def api_request(url: str, querystring: dict) -> Optional[dict]:
    """
    Функция отправки запроса к API
    :param url: url запроса
    :param querystring: параметр запроса в формате словаря
    """
    try:
        response = requests.request("GET", url, headers=config.headers, params=querystring, timeout=20)
        if response.status_code == 200:
            result = json.loads(response.text)
        else:
            result = None
    except requests.Timeout as time_end:
        logger.exception(time_end)
        result = None
    except requests.RequestException as er:
        logger.exception(er)
        result = None

    return result


def location_search(my_city: str) -> Optional[dict]:
    """
    Функция для поиска города по названию
    :param my_city: название города
    :return: данные в формате json либо None при отсутствии города в даных от API
    """
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": my_city, "locale": "ru_RU"}

    return api_request(url=url, querystring=querystring)


def hotels_search(city_id: str, price=None) -> Optional[dict]:
    """
    Функция для поиска отелей по id города
    :param price: список с диапазоном цен
    :param city_id: id города
    :return: данные в формате json либо None при отсутствии ответа от API
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    check_in = datetime.now()
    check_out = check_in + timedelta(days=7)
    check_in = check_in.strftime('%Y-%m-%d')
    check_out = check_out.strftime('%Y-%m-%d')

    querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                   "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE",
                   "locale": "ru_RU", "currency": "USD"}

    if price:
        price_max = price[1]
        price_min = price[0]
        if price_min > price_max:
            price_min, price_max = price_max, price_min
        querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                       "checkOut": check_out, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                       "sortOrder": "PRICE", "locale": "ru_RU", "currency": "USD"}

    return api_request(url=url, querystring=querystring)


def photo_search(hotel_id: str) -> Optional[dict]:
    """
    Функция для получения данных в формате json с url фото отеля
    :param hotel_id: id отеля
    :return: словарь
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}

    return api_request(url=url, querystring=querystring)
