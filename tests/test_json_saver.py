import pytest

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


def test_json_saver_read(tmp_path: Path) -> None:
    path = tmp_path / "aeroread.json"
    path.write_text('{"a": 1}', encoding="utf-8")
    json_saver = JsonSaver(file_path=str(path))
    assert json_saver._read() == []
    path.write_text('[{"callsign": "EWG6SW  ", "origin_country": "Germany",'
                    ' "baro_altitude": 9098.28, "velocity": 212.48}]', encoding='utf-8')
    assert json_saver._read() == [{"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28,
                                   "velocity": 212.48}]


def test_json_saver_write(tmp_path: Path, data: list) -> None:
    path = tmp_path / "aerowrite.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write(data)
    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_del_aeroplanes(tmp_path: Path, data: list) -> None:
    path = tmp_path / "aerodelete.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write(data)
    json_saver.del_aeroplanes(callsign="EWG6SW  ")
    assert json_saver._read() == [{"callsign": "EZY46RQ ", "origin_country": "United Kingdom", "baro_altitude": 11277.6,
                                   "velocity": 241.56},
                                  {"callsign": "EJU68XU ", "origin_country": "Austria", "baro_altitude": 11902.44,
                                   "velocity": 216.87}]
    json_saver.del_aeroplanes()
    assert json_saver._read() == []

def test_get_aeroplanes(tmp_path: Path, data: list) -> None:
    path = tmp_path / "aeroget.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write(data)
    aeroplanes_list = [Aeroplane(**item) for item in data]
    assert json_saver.get_aeroplanes() == aeroplanes_list
    assert json_saver.get_aeroplanes(callsign="EWG6SW  ") == [Aeroplane(**data[0])]
    assert json_saver.get_aeroplanes(origin_country="United Kingdom") == [Aeroplane(**data[1])]
    assert json_saver.get_aeroplanes(baro_altitude=9098.28) == [Aeroplane(**data[0])]
    assert json_saver.get_aeroplanes(velocity=241.56) == [Aeroplane(**data[1])]

def test_add_aeroplanes(tmp_path: Path, data: list) -> None:
    path = tmp_path / "aeroadd.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver.add_aeroplane(Aeroplane(**data[0]))
    assert json_saver.get_aeroplanes() == [Aeroplane(**data[0])]
    json_saver.add_aeroplanes([Aeroplane(**item) for item in data[1:]])
    assert json_saver.get_aeroplanes() == [Aeroplane(**item) for item in data]


def test_add_aeroplanes_wrong(tmp_path: Path) -> None:
    path = tmp_path / "aeroaddwrong.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver.add_aeroplanes([])
    assert json_saver.get_aeroplanes() == []
    with pytest.raises(TypeError):
        json_saver.add_aeroplanes([1, 2, 3])
    with pytest.raises(TypeError):
        json_saver.add_aeroplanes(1)