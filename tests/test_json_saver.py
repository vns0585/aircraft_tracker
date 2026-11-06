from src.json_saver import JsonSaver
from src.aeroplane import Aeroplane
import json
from pathlib import Path


def test_json_saver_init(tmp_path: Path) -> None:
    path = tmp_path / "aeroinit.json"
    JsonSaver(file_path=str(path))
    assert json.loads(path.read_text(encoding="utf-8")) == []
    path.write_text('[{"callsign": "EWG6SW  ", "origin_country": "Germany",'
                    ' "baro_altitude": 9098.28, "velocity": 212.48}]', encoding='utf-8')
    JsonSaver(file_path=str(path))
    assert json.loads(path.read_text(encoding="utf-8")) == [{"callsign": "EWG6SW  ", "origin_country": "Germany",
                                                             "baro_altitude": 9098.28, "velocity": 212.48}]


def test_read(tmp_path: Path) -> None:
    path = tmp_path / "aeroread.json"
    path.write_text('{"a": 1}', encoding="utf-8")
    json_saver = JsonSaver(file_path=str(path))
    assert json_saver._read() == []
    path.write_text('[{"callsign": "EWG6SW  ", "origin_country": "Germany",'
                    ' "baro_altitude": 9098.28, "velocity": 212.48}]', encoding='utf-8')
    assert json_saver._read() == [{"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28,
                                   "velocity": 212.48}]


def test_write(tmp_path: Path) -> None:
    path = tmp_path / "aerowrite.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write([{"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28,
                                   "velocity": 212.48}])
    assert json.loads(path.read_text(encoding="utf-8")) == [{"callsign": "EWG6SW  ", "origin_country": "Germany",
                                                             "baro_altitude": 9098.28, "velocity": 212.48}]


def test_delete(tmp_path: Path) -> None:
    path = tmp_path / "aerodelete.json"
