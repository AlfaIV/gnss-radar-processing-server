from astropy.time import Time
from astropy import units as u
from sgp4.api import Satrec
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation, EarthLocation, ITRS, SkyCoord, AltAz, Distance
import numpy as np

class SatellitesPositions:
    def __init__(self):
        self.satellites_positions = {}
        self.satellites_names = []
        self.sattelites_count = 0
        self.satellites_names.append("A")
        self.satellites_names.append("B")
    
    def get_sattelites_positions(self):
        
        tle_file = 'datasets\TLE\gps.tle'
        with open(tle_file, 'r') as file:
            TLE_array = []
            for line in file:
                words = line.split()
                if (words[0] == '1'):
                    TLE_array[-1].line1 = line
                elif (words[0] == '2'):
                    TLE_array[-1].line2 = line
                else:
                    TLE_array.append(TLE(line))
        
        satellite = Satrec.twoline2rv(TLE_array[-1].line1, TLE_array[-1].line2)
        # получиить время пргедсказания
        current_time = Time.now()
        error_code, teme_p, teme_v = satellite.sgp4(current_time.jd1, current_time.jd2)  # in km and km/s
        if error_code != 0:
            raise RuntimeError(SGP4_ERRORS[error_code])
        
        teme_p = CartesianRepresentation(teme_p*u.km)
        teme_v = CartesianDifferential(teme_v*u.km/u.s)
        teme = TEME(teme_p.with_differentials(teme_v), obstime=current_time)

        itrs_geo =  teme.transform_to(ITRS(obstime=current_time))
        location = itrs_geo.earth_location
        location.geodetic 

        # Определение позиции наблюдателя на Земле
        observer_lat = 52 * u.deg  # Широта наблюдателя (например, Москва)
        observer_lon = 38 * u.deg  # Долгота наблюдателя
        observer_height = 0 * u.km  # Высота над уровнем моря

        # Конвертация широты/долготы наблюдателя в ITRS
        observer_location = EarthLocation.from_geodetic(observer_lon, observer_lat, observer_height)
        observer_itrs = observer_location.get_itrs(obstime=current_time)

        # Нахождение угла между наблюдателем и спутником
        separation_angle = observer_itrs.separation(itrs_geo)

        # Вывод результата
        print(f"Угол между наблюдателем и спутником: {separation_angle.to(u.deg):.2f} градусов")

        # Преобразование в AltAz для получения азимута и угла места
        altaz_frame = AltAz(obstime=current_time, location=observer_location)
        satellite_altaz = itrs_geo.transform_to(altaz_frame)

        # Получение азимута и угла места
        azimuth = satellite_altaz.az
        elevation = satellite_altaz.alt

        print(f"Азимут: {azimuth.to(u.deg):.2f} градусов")
        print(f"Угол места: {elevation.to(u.deg):.2f} градусов")    

        # Вычисление евклидова расстояния
        distance_value = np.sqrt((itrs_geo.x - observer_itrs.x)**2 + 
                                (itrs_geo.y - observer_itrs.y)**2 + 
                                (itrs_geo.z - observer_itrs.z)**2)
        # Создание объекта Distance
        distance = Distance(value=distance_value, unit = u.m)  # Преобразуем в метры

        print(f"Дальность до спутника: {distance.to(u.km):.2f} километров")