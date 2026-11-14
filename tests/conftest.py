import pytest

from src.aeroplane import Aeroplane


@pytest.fixture
def object_list() -> list:
    return [
        ['4d012d', 'CLX9723 ', 'Luxembourg', 1793779439, 1793779439, 6.2116, 49.6293, None, True, 5.92, 244.69, None, None, None, None, False, 0],
        ['3d6954', 'DFMDG   ', 'Germany', 1793779455, 1793779456, 6.1768, 49.9089, 8229.6, False, 139.87, 150.23, 0, None, 8298.18, '0110', False, 0],
        ['a71970', 'N557AD  ', 'United States', 1793779268, 1793779268, 6.2085, 49.6283, 9026.6, False, 146.17, 64.69, None, None, None, '2216', False, 0]
    ]


@pytest.fixture
def data() -> list:
    return [{"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28, "velocity": 212.48},
            {"callsign": "EZY46RQ ", "origin_country": "United Kingdom", "baro_altitude": 11277.6, "velocity": 241.56},
            {"callsign": "EJU68XU ", "origin_country": "Austria", "baro_altitude": 11902.44, "velocity": 216.87}]


@pytest.fixture
def sorted_data_by_altitude_dsc() -> list:
    return [{"callsign": "EJU68XU ", "origin_country": "Austria", "baro_altitude": 11902.44, "velocity": 216.87},
            {"callsign": "EZY46RQ ", "origin_country": "United Kingdom", "baro_altitude": 11277.6, "velocity": 241.56},
            {"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28, "velocity": 212.48}]


@pytest.fixture
def filtered_data() -> dict:
    return {"callsign": "EWG6SW  ", "origin_country": "Germany", "baro_altitude": 9098.28, "velocity": 212.48}