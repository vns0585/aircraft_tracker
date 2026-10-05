from datetime import datetime
from typing import Dict, Union

from requests import get

from src.base_api_client import BaseApiClient


class ApiClient(BaseApiClient):
    __api_url_coordinates: str
    __api_url_aeroplanes: str
    aeroplanes: list
    last_request_time: datetime

    def __init__(self) -> None:
        self.__api_url_coordinates = 'https://nominatim.openstreetmap.org/search'
        self.__api_url_aeroplanes = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = []

    def get_geo_coordinates(self, country: str) -> list:
        # URL API-сервиса для определения координат
        url = self.__api_url_coordinates

        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers = {
            'User-Agent': 'test-app/1.0',
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params: Dict[str, Union[str, int]] = {
            'country': country,
            'format': 'json',
            'limit': 1
        }

        response = get(url=url, params=params, headers=headers)
        data = response.json()
        geo_coordinates = data[0].get('boundingbox')
        if isinstance(geo_coordinates, list):
            return geo_coordinates
        else:
            return []

    def get_aeroplanes(self, geo_coordinates: list) -> list:
        # URL API-сервиса для получения списка самолетов по координатам области
        url = self.__api_url_aeroplanes

        # Параметры для фильтрации самолетов по их географическим координатам.
        try:
            params = {
                'lamin': geo_coordinates[0],
                'lamax': geo_coordinates[1],
                'lomin': geo_coordinates[2],
                'lomax': geo_coordinates[3],
            }
        except KeyError as e:
            print("Неверный формат координат для получения списка самолетов", e)
            return []

        response = get(url=url, params=params)
        self.last_request_time = datetime.now()
        self.aeroplanes = response.json().get('states')
        return self.aeroplanes


if __name__ == '__main__':
    api = ApiClient()
    geo = api.get_geo_coordinates("Luxembourg")
    print(geo)
    planes = api.get_aeroplanes(geo)
    print(planes)
