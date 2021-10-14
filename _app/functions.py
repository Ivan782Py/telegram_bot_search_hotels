from typing import Optional

from _app import req
import re


def value_search(data: any, i_key: str) -> any:
    """
    Функция для рекурсивного поиска значения во вложенных массивах (dict, list).
    :param data: массив данных
    :param i_key: ключ
    :return: значение по ключу
    """
    if i_key in data:
        return data[i_key]

    for key, value in data.items():
        if isinstance(value, dict):
            result = value_search(value, i_key)
            if result is not None:
                return result
        elif isinstance(value, list):
            for i in range(len(value)):
                result = value_search(value[i], i_key)
                if result is not None:
                    return result

    return None


def city_check(city_name: str) -> bool:
    """
    Функция для проверки наличия города в базе API Hotels
    :param city_name: название города
    :return: bool
    """
    i_data = req.location_search(my_city=city_name)
    result = value_search(data=i_data, i_key='entities')
    if result:
        return True
    else:
        return False


def get_hotels(city: str, num_hotels: str, i_command: str,
               choice_price: list = None, distance: list = None) -> callable:
    """
    Функция приема параметров от бота и вызова функции обработки ответа my_hotels()
    :param city: название города
    :param num_hotels: количество отелей
    :param i_command: команда бота
    :param choice_price: диапазон цен
    :param distance: расстояние от отеля до центра
    :return: функцию обработки ответа, либо None при ошибке ответа от API
    """
    i_data = req.location_search(my_city=city)
    city_id = value_search(data=i_data, i_key='destinationId')
    get_req = req.hotels_search(city_id=city_id, price=choice_price)
    hotels_list = value_search(data=get_req, i_key='results')

    i_command = i_command[1:]
    data = {'id': [], 'name': [], 'address': [], 'distance': [], 'price': []}
    try:
        for elem in hotels_list:
            data['id'].append(value_search(data=elem, i_key='id'))
            data['name'].append(value_search(data=elem, i_key='name'))
            data['address'].append(value_search(data=elem, i_key='streetAddress'))
            data['distance'].append(value_search(data=elem, i_key='distance'))
            data['price'].append(value_search(data=elem, i_key='exactCurrent'))
    except:
        return None

    return my_hotels(data=data, number=num_hotels,
                     choice=i_command, diapason=distance
                     )


def my_hotels(data: dict, number: str, choice: str, diapason: list) -> Optional[dict[str, list]]:
    """
    Функция для обработки ответа в соответствии с командой от юзера чата
    :param data: словарь с данными по отелям в городе
    :param number: число отелей для ответа
    :param choice: команда от юзера
    :param diapason: расстояние от отеля до центра
    :return:
    """
    result = {'name': [],
              'address': [],
              'distance': [],
              'price': [],
              'id': []
              }

    i_index = 0
    if choice == 'highprice':
        i_index = -1
    elif choice == 'bestdeal':
        data: dict = best_deal(data=data, my_range=diapason, number=number)
        number = len(data['id'])
    if number == 0:
        return None

    for _ in range(int(number)):
        result['name'].append(data['name'].pop(i_index))
        result['address'].append(data['address'].pop(i_index))
        result['distance'].append(data['distance'].pop(i_index))
        result['price'].append(data['price'].pop(i_index))
        result['id'].append(data['id'].pop(i_index))

    return result


def best_deal(data, my_range, number):
    """
    Функция обработки команды bestdeal - поиск отелей в указанном диапазоне my_range
    :param data: словарь с данными по отелям в городе в указанном диапазоне цен
    :param my_range: диапазон расстояния от отеля до центра города
    :param number: количество отелей
    :return: словарь с отфильтрованными отелями
    """
    dist = data['distance']
    dist_list = []
    for i in dist:
        new_elem = re.findall(r"\d+(?:\.\d+)?", i)
        dist_list.append(float(new_elem[0]))

    if float(my_range[0]) > float(my_range[1]):
        my_range[0], my_range[1] = my_range[1], my_range[0]

    min_num = float(my_range[0])
    max_num = float(my_range[1])
    number = int(number)
    dist_index_list = []

    for i_num in dist_list:
        if number == 0:
            break
        elif min_num <= i_num <= max_num:
            dist_index_list.append(dist_list.index(i_num))
        number -= 1

    if dist_index_list:
        for key in data:
            data[key] = [x for x in data[key] if data[key].index(x) in dist_index_list]

    return data


def get_photo(hotel_id, total):
    """
    Функция для получения фото по id города
    :param hotel_id: id города
    :param total: количество фотографий
    :return:
    """
    total = int(total)

    try:
        get_req = req.photo_search(hotel_id=hotel_id)
        photo_list = value_search(data=get_req, i_key='hotelImages')
    except Exception:
        return None

    url_list = []
    for elem in photo_list:
        if total == 0:
            break
        i_url = value_search(data=elem, i_key='baseUrl')[:-10] + 'z.jpg'
        url_list.append(i_url)
        total -= 1
    return url_list
