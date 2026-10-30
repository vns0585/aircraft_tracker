import re

from src.aeroplane import Aeroplane
from src.api_client import ApiClient
from src.json_saver import JsonSaver


def get_top_aeroplanes(aeroplanes_list: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    if top_n < 1:
        return []
    if len(aeroplanes_list) < 2:
        return aeroplanes_list
    sorted_aeroplanes = sorted(aeroplanes_list, key=lambda a: a.baro_altitude, reverse=True)
    if top_n > len(sorted_aeroplanes):
        return sorted_aeroplanes
    else:
        return sorted_aeroplanes[:top_n]


def filter_aeroplanes(aeroplanes_list: list[Aeroplane], filter_words: list[str]) -> list[Aeroplane]:
    if not filter_words:
        return aeroplanes_list
    if len(aeroplanes_list) < 1:
        return aeroplanes_list
    filtered_aeroplanes_list = list(filter(lambda x: x.origin_country in filter_words, aeroplanes_list))
    return filtered_aeroplanes_list


def user_interaction() -> None:
    api = ApiClient()
    while True:
        country = input("Введите название страны: ")
        if re.fullmatch(r"[^\W\d_][\w\s\-']*", country, re.UNICODE):
            geo_coordinates = api.get_geo_coordinates(country)
            if not geo_coordinates:
                print(f'Не найдены координаты страны {country}! Попробуйте ввести другую страну.')
                continue
            break
        print('Название страны может содержать только буквы, пробелы, тире и апостроф!')

    while True:
        try:
            top_n = int(input("Введите количество самолетов для вывода в топ N по высоте: "))
        except ValueError:
            print('Ожидается целое число!')
            continue
        else:
            if top_n < 1:
                print('Ожидается значение больше 0!')
                continue
            break

    while True:
        filter_word = input("Введите название страны регистрации самолетов для фильтрации: ")
        if re.fullmatch(r"[^\W\d_][\w\s\-']*", filter_word, re.UNICODE):
            break
        print('Название страны может содержать только буквы, пробелы, тире и апостроф!')

    # Получение информации о самолетах
    aeroplanes = api.get_aeroplanes(geo_coordinates)
    if not aeroplanes:
        print(f'Нет информации о самолетах над {country}')
        return
    aeroplanes_list = Aeroplane.cast_to_object_list(aeroplanes)

    # Сохранение информации в файл
    json_saver = JsonSaver()
    json_saver.add_aeroplanes(aeroplanes_list)

    # Получение топ-n самолетов по высоте
    sorted_aeroplanes = get_top_aeroplanes(aeroplanes_list, top_n)
    print(f'\nТОП-{top_n} самолетов по высоте полета:')
    for i in range(len(sorted_aeroplanes)):
        print(f'{i+1}. Позывной: {sorted_aeroplanes[i].callsign}, Высота: {sorted_aeroplanes[i].baro_altitude} м')

    # Фильтрация по стране регистрации
    filtered_aeroplanes = filter_aeroplanes(aeroplanes_list, [filter_word])
    print(f'\nСамолеты зарегистрированные в стране {filter_word}: ')
    for i in range(len(filtered_aeroplanes)):
        print(f'{i+1}. Позывной: {filtered_aeroplanes[i].callsign},'
              f' Страна регистрации: {filtered_aeroplanes[i].origin_country}')


if __name__ == '__main__':
    user_interaction()
