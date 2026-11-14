from pathlib import Path

import pytest

from main import get_top_aeroplanes, filter_aeroplanes
from src.aeroplane import Aeroplane
from src.json_saver import JsonSaver


def test_get_top_aeroplanes(tmp_path: Path, data: list, sorted_data_by_altitude_dsc: list) -> None:
    path = tmp_path / "aerotop.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write(data)
    aeroplanes_list = json_saver.get_aeroplanes()
    json_saver.del_aeroplanes()
    json_saver._write(sorted_data_by_altitude_dsc)
    aeroplanes_list_sorted = json_saver.get_aeroplanes()
    assert get_top_aeroplanes(aeroplanes_list,3) == aeroplanes_list_sorted
    assert get_top_aeroplanes(aeroplanes_list,2) == aeroplanes_list_sorted[:2]
    assert get_top_aeroplanes(aeroplanes_list,1) == aeroplanes_list_sorted[:1]
    assert get_top_aeroplanes(aeroplanes_list,0) == []
    assert get_top_aeroplanes(aeroplanes_list,4) == aeroplanes_list_sorted
    assert get_top_aeroplanes([aeroplanes_list[0]],5) == [aeroplanes_list[0]]
    with pytest.raises(TypeError):
        get_top_aeroplanes([1, 2, 3], 5)


def test_filter_aeroplanes(tmp_path: Path, data: list, filtered_data: dict) -> None:
    path = tmp_path / "aerotop.json"
    json_saver = JsonSaver(file_path=str(path))
    json_saver._write(data)
    aeroplanes_list = json_saver.get_aeroplanes()
    assert filter_aeroplanes(aeroplanes_list, ["Germany"]) == [Aeroplane(**filtered_data)]
    assert filter_aeroplanes(aeroplanes_list, []) == aeroplanes_list
    assert filter_aeroplanes([], ["Germany"]) == []
    with pytest.raises(TypeError):
        filter_aeroplanes([1, 2, 3], ["Germany"])