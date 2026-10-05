from abc import ABC, abstractmethod


class BaseSaver(ABC):

    @abstractmethod
    def add_aeroplane(self, aeroplane_data: dict) -> None:
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: dict) -> list:
        pass

    @abstractmethod
    def del_aeroplanes(self, **criteria: dict) -> int:
        pass
