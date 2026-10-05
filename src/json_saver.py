import json
import os

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

    def add_aeroplane(self, aeroplane_data: dict) -> None:
        data = self._read()
        data.append(aeroplane_data)
        self._write(data)

    def get_aeroplanes(self, **criteria: dict) -> list:
        data = self._read()
        if not criteria:
            return data
        return [
            item for item in data
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
