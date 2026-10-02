from abc import ABC, abstractmethod


class BaseApiClient(ABC):

    @abstractmethod
    def get_geo_coordinates(self, country: str) -> list:
        pass

    @abstractmethod
    def get_aeroplanes(self, geo_coordinates: list) -> list:
        pass
