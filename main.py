import re
from src.aeroplane import Aeroplane
from src.api_client import ApiClient
from src.json_saver import JsonSaver


def get_top_aeroplanes(aeroplanes_list: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    if top_n < 1:
        return []
    if len(aeroplanes_list) < 2:
        return aeroplanes_list
    sorted_aeroplanes = sorted(aeroplanes_list, reverse=True)
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
    top_n: int
    api = ApiClient()
    while True:
        country = input("Введите название страны: ")
        if bool(re.fullmatch(r"[^\W\d_][\w\s\-']*", country, re.UNICODE)):
            geo_coordinates = api.get_geo_coordinates(country)
            if not geo_coordinates:
                print(f'Не найдены координаты страны {country}! Попробуйте ввести другую страну.')
                continue
            break
        print('Название страны должно состоять из букв!')
    while True:
        try:
            top_n = int(input("Введите количество самолетов для вывода в топ N: "))
        except ValueError:
            print('Ожидается целое число!')
            continue
        else:
            if top_n < 1:
                print('Ожидается значение больше 0!')
                continue
            break

    while True:
        filter_words = input("Введите названия стран для фильтрации по стране регистрации"
                             " (разделенные пробелом): ").split()
        for word in filter_words:
            if word.isalpha():
                continue
            else:
                print('Названия стран должны состоять из букв!')
                break
        else:
            break

    while True:
        altitude_range = input("Введите диапазон высот полета (разделенные тире \"-\"): ").split('-')  # Пример: 100000 - 150000
        try:
            altitude_range = [int(i.strip()) for i in altitude_range]
        except ValueError:
            continue
        else:
            if len(altitude_range) != 2:
                print('Ожидаются два положительных целых числа разделенные тире!')
                continue
            break

    # Получение информации о самолетах
    aeroplanes = api.get_aeroplanes(geo_coordinates)
    if not aeroplanes:
        print(f'Нет информации о самолетах над {country}')
        return
    aeroplanes_list = Aeroplane.cast_to_object_list(aeroplanes)

    # Сохранение информации в файл
    json_saver = JsonSaver()
    json_saver.add_aeroplanes(aeroplanes_list)

    sorted_aeroplanes = get_top_aeroplanes(aeroplanes_list, top_n)
    print(f'ТОП-{top_n} самолетов по скорости полета:')
    for i in range(len(sorted_aeroplanes)):
        print(f'{i+1}. Позывной: {sorted_aeroplanes[i].callsign}, Скорость: {sorted_aeroplanes[i].velocity} м/с')

    filtered_aeroplanes = filter_aeroplanes(aeroplanes_list, filter_words)
    for aeroplane in filtered_aeroplanes:
        print(aeroplane.origin_country)



if __name__ == '__main__':
    user_interaction()
