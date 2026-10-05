from abc import ABC, abstractmethod
from src.aeroplane import Aeroplane

class BaseSaver(ABC):

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: dict) -> list:
        pass

    @abstractmethod
    def del_aeroplanes(self, **criteria: dict) -> int:
        pass
