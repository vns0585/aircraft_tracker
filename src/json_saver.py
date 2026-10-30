import json
import os

from src.aeroplane import Aeroplane
from src.base_saver import BaseSaver


class JsonSaver(BaseSaver):

    def __init__(self, file_path: str = "data/aeroplanes.json") -> None:
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _read(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as file:
            result = json.load(file)
        if isinstance(result, list):
            return result
        else:
            return []

    def _write(self, data: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        self.add_aeroplanes([aeroplane])

    def add_aeroplanes(self, aeroplanes_list: list[Aeroplane]) -> None:
        if not aeroplanes_list:
            return
        if not all(isinstance(item, Aeroplane) for item in aeroplanes_list):
            raise TypeError(f"Ожидался список Aeroplane, получены: "
                            f"{[type(a).__name__ for a in aeroplanes_list if not isinstance(a, Aeroplane)]}"
                            )
        data = self._read()
        new_callsigns = {str(vars(aeroplane).get("callsign")) for aeroplane in aeroplanes_list}
        data = [item for item in data if str(item.get("callsign")) not in new_callsigns]
        data.extend(vars(aeroplane) for aeroplane in aeroplanes_list)
        self._write(data)

    def get_aeroplanes(self, **criteria: dict) -> list:
        data = self._read()
        if not criteria:
            return data
        return [
            Aeroplane(**item) for item in data
            if all(str(item.get(key)) == str(value) for key, value in criteria.items())
        ]

    def del_aeroplanes(self, **criteria: dict) -> int:
        data = self._read()
        if not criteria:
            self._write([])
            return len(data)

        kept = [
            item for item in data
            if all(str(item.get(key)) == str(value) for key, value in criteria.items())
        ]
        deleted = len(data) - len(kept)
        self._write(kept)
        return deleted
