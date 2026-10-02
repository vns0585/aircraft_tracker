class Aeroplane:
    # 0. Unique ICAO 24-bit address of the transponder in hex string representation.
    #icao24: str

    # 1. Callsign of the vehicle (8 chars). Can be null if no callsign has been received.
    callsign: str

    # 2. Country name inferred from the ICAO 24-bit address.
    origin_country: str

    # 3. Unix timestamp (seconds) for the last position update. Can be null if no position report was received by
    # OpenSky within the past 15s.
    #time_position: int

    # 4. Unix timestamp (seconds) for the last update in general. This field is updated for any new, valid message
    # received from the transponder.
    #last_contact: int

    # 5. WGS-84 longitude in decimal degrees. Can be null.
    #longitude: float

    # 6. WGS-84 latitude in decimal degrees. Can be null.
    #latitude: float

    # 7. Barometric altitude in meters. Can be null.
    baro_altitude: float

    # 8. Boolean value which indicates if the position was retrieved from a surface position report.
    #on_ground: bool

    # 9. Velocity over ground in m/s. Can be null.
    velocity: float

    # 10. True track in decimal degrees clockwise from north (north=0°). Can be null.
    #true_track: float

    # 11. Vertical rate in m/s. A positive value indicates that the airplane is climbing, a negative value indicates
    # that it descends. Can be null.
    #vertical_rate: float

    # 12. IDs of the receivers which contributed to this state vector. Is null if no filtering for sensor was used
    # in the request.
    #sensors: int

    # 13. Geometric altitude in meters. Can be null.
    #geo_altitude: float

    # 14. The transponder code aka Squawk. Can be null.
    #squawk: str

    # 15. Whether flight status indicates special purpose indicator.
    #spi: bool

    # 16. Origin of this state’s position.
    # 0 = ADS-B
    # 1 = ASTERIX
    # 2 = MLAT
    # 3 = FLARM
    #position_source: int

    def __init__(self, callsign: str, origin_country: str, baro_altitude: float, velocity: float) -> None:
        self.callsign = callsign if isinstance(callsign, str) and len(callsign) == 8 else ""
        self.origin_country = origin_country if isinstance(origin_country, str) else ""
        # Используем барометрическую высоту, т.к. используется для эшелонирования в авиации
        self.baro_altitude = baro_altitude if isinstance(baro_altitude, float) and baro_altitude >= 0 else 0
        self.velocity = velocity if isinstance(velocity, float) and velocity >= 0 else 0

    @staticmethod
    def cast_to_object_list(aeroplanes_list: list) -> list:
        object_list = []
        for item in aeroplanes_list:
            object_list.append(Aeroplane(item[1], item[2], item[7], item[9]))
        return object_list
