import pytest
from src.aeroplane import Aeroplane


def test_aeroplane_init() -> None:
    a1 = Aeroplane('AFR1434 ','France', 11353.8, 158.42)
    assert a1.baro_altitude == 11353.8
    assert a1.velocity == 158.42
    assert a1.origin_country == 'France'
    assert a1.callsign == 'AFR1434 '


def test_aeroplane_init_wrong() -> None:
    a2 = Aeroplane('AFR1434',10, -11353.8, -158.42)
    assert a2.baro_altitude == 0
    assert a2.velocity == 0
    assert a2.origin_country == ''
    assert a2.callsign == ''


def test_cast_to_object_list(object_list: list) -> None:
    obj_lst = Aeroplane.cast_to_object_list(object_list)
    for i in range(len(obj_lst)):
        assert type(obj_lst[i]) == Aeroplane
        assert obj_lst[i].callsign == object_list[i][1]
        assert obj_lst[i].origin_country == object_list[i][2]
        assert obj_lst[i].baro_altitude == object_list[i][7] or (obj_lst[i].baro_altitude == 0 and object_list[i][7] is None)
        assert obj_lst[i].velocity == object_list[i][9]


def test_cast_to_object_list_wrong() -> None:
    obj_lst = Aeroplane.cast_to_object_list([[0,1,2]])
    assert obj_lst == []
    obj_lst = Aeroplane.cast_to_object_list([])
    assert obj_lst == []
    obj_lst = Aeroplane.cast_to_object_list({})
    assert obj_lst == []


def test_comparisons() -> None:
    a1 = Aeroplane('AFR1434 ','France', 353.8, 46.11)
    a2 = Aeroplane('AFR1434 ','France', 11353.8, 158.42)
    a3 = Aeroplane('AFR1434 ','France', 11253.8, 158.42)
    assert a1 < a2
    assert a2 == a3
    assert a3 != a1
    assert a2 <= a3
    assert a2 >= a3
    assert a3 > a1

    assert a1.is_lower_than(a2)
    assert a2.is_higher_than(a1)
    assert a2.at_same_altitude(a3)


def test_comparisons_wrong() -> None:
    a1 = Aeroplane('AFR1434 ', 'France', 353.8, 46.11)
    a2 = Aeroplane('AFR1434 ', 'France', 11353.8, 158.42)

    assert a1.__eq__(1) is NotImplemented
    assert a1.__lt__(1) is NotImplemented
    assert a1.__gt__(1) is NotImplemented
    assert a1.__ge__(1) is NotImplemented
    assert a1.__le__(1) is NotImplemented
    assert a1.__ne__(1) is NotImplemented

    with pytest.raises(ValueError):
        a1.is_lower_than(a2,-1)
    with pytest.raises(ValueError):
        a1.is_higher_than(a2,-1)
    with pytest.raises(ValueError):
        a1.at_same_altitude(a2,-1)

    with pytest.raises(TypeError):
        a1.is_lower_than(1)
    with pytest.raises(TypeError):
        a1.is_higher_than(1)
    with pytest.raises(TypeError):
        a1.at_same_altitude(1)


def test_hash() -> None:
    a1 = Aeroplane('AFR1434 ', 'France', 353.8, 46.11)
    a11 = Aeroplane('AFR1434 ', 'France', 353.8, 46.11)
    assert hash(a1) == hash(a11)