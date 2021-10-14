import requests
import json
from datetime import datetime, timedelta


def location_search(my_city: str) -> dict:
    """
    Функция для поиска города по названию
    :param my_city: название города
    :return: данные в формате json
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": my_city, "locale": "en_US"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "24edd3a4d4mshd18ba19942cd8bbp153e13jsnd97a92cb7c95"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    return result


def hotels_search(city_id: str, price=None) -> dict:
    """
    Функция для поиска отелей по id города
    :param price: список с диапазоном цен
    :param city_id: id города
    :return: данные в формате json
    """

    url = "https://hotels4.p.rapidapi.com/properties/list"
    check_in = datetime.now()
    check_out = check_in + timedelta(days=7)
    check_in = check_in.strftime('%Y-%m-%d')
    check_out = check_out.strftime('%Y-%m-%d')

    if price is None:
        querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                       "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE",
                       "locale": "en_US", "currency": "USD"}
    else:
        price_max = price[1]
        price_min = price[0]
        if price_min > price_max:
            price_min, price_max = price_max, price_min
        querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
                       "checkOut": check_out, "adults1": "1", "priceMin": price_min, "priceMax": price_max,
                       "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "24edd3a4d4mshd18ba19942cd8bbp153e13jsnd97a92cb7c95"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    return result


def photo_search(hotel_id: str) -> dict:
    """
    Функция для получения данных в формате json с url фото отеля
    :param hotel_id: id отеля
    :return: словарь
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "24edd3a4d4mshd18ba19942cd8bbp153e13jsnd97a92cb7c95"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    return result
