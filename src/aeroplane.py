from functools import total_ordering


@total_ordering
class Aeroplane:

    # Позывной рейса (8 символов).
    callsign: str

    # Страна регистрации ВС
    origin_country: str

    # Барометрическая высота (м) (используется для вертикального эшелонирования)
    baro_altitude: float

    # Горизонтальная скорость (м/с)
    velocity: float

    # Минимальный стандартный интервал вертикального эшелонирования (м) (1000 футов ~ 304.8 метра)
    ALTITUDE_TOLERANCE = 304.8

    def __init__(self, callsign: str, origin_country: str, baro_altitude: float, velocity: float) -> None:
        self.callsign = callsign if isinstance(callsign, str) and len(callsign) == 8 else ""
        self.origin_country = origin_country if isinstance(origin_country, str) else ""
        self.baro_altitude = baro_altitude if isinstance(baro_altitude, float) and baro_altitude >= 0 else 0
        self.velocity = velocity if isinstance(velocity, float) and velocity >= 0 else 0

    @staticmethod
    def cast_to_object_list(aeroplanes_list: list) -> list:
        object_list = []
        for item in aeroplanes_list:
            object_list.append(Aeroplane(item[1], item[2], item[7], item[9]))
        return object_list

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    # __le__, __gt__, __ge__, __ne__ достроит total_ordering

    def __hash__(self):
        return hash(self.velocity)

    def is_higher_than(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError(f"Ожидается объект класса Aeroplane, а предоставлен {type(other).__name__}")
        return self.baro_altitude - other.baro_altitude > self.ALTITUDE_TOLERANCE

    def is_lower_than(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError(f"Ожидается объект класса Aeroplane, а предоставлен {type(other).__name__}")
        return other.baro_altitude - self.baro_altitude > self.ALTITUDE_TOLERANCE

    def at_same_altitude(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError(f"Ожидается объект класса Aeroplane, а предоставлен {type(other).__name__}")
        return abs(self.baro_altitude - other.baro_altitude) <= self.ALTITUDE_TOLERANCE
