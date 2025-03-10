import os
from app.core.config import configs

from astropy.time import Time
from astropy import units as u
from sgp4.api import Satrec
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation, EarthLocation, ITRS, AltAz, Distance

from app.schemas.sattelites_position import RadarPositionRequest, SatellitesPositionResponce
from app.entities.sattellites import TLE, SatellitePosition, SatellitesPosition
from datetime import datetime
import numpy as np

class SatellitesPositions:
    def __init__(self):
        tle_file = os.path.join(configs.PROJECT_ROOT ,'app' ,'services' ,'tle' ,'gps.tle')
        self.TLE_array = []
        with open(tle_file, 'r') as file:
            for line in file:
                words = line.split()
                if (words[0] == '1'):
                    self.TLE_array[-1].line1 = line
                elif (words[0] == '2'):
                    self.TLE_array[-1].line2 = line
                else:
                    self.TLE_array.append(TLE(line))
                    print(f'name: {self.TLE_array[-1].name}')
        
        self.satellites = []
        for tle in self.TLE_array:
            self.satellites.append({
                'satrec': Satrec.twoline2rv(tle.line1, tle.line2),
                                     'tle': tle
                                     })
        
    
    def get_sattelites_positions(self, radar: RadarPositionRequest) -> SatellitesPositionResponce:
        current_time = Time.now()
        
        radar_position = {
            'radar_x': 2842957.63,
            'radar_y': 2160952.62,
            'radar_z': 5265993.63,
        }

        satellite_positions = []

        for satellite in self.satellites:
            sattelite_props = self.get_sattelite_positions(current_time, satellite['satrec'], radar_position)
            name = satellite['tle'].name.strip()
            parts = name.split()
            grouping = parts[0]
            satellite_name = " ".join(parts[1:])
            satellite_positions.append({
                'Group': grouping,
                'Name': satellite_name,
                'Azimuth': round(sattelite_props['Azimuth'].degree, 2),
                'Range': round(sattelite_props['Range'].km, 2),
                })

        return {
            'Satellites': satellite_positions
        }

    def get_sattelite_positions(self, current_time: datetime, satellite: object, observer: RadarPositionRequest) -> SatellitePosition:
        error_code, teme_p, teme_v = satellite.sgp4(current_time.jd1, current_time.jd2)  # in km and km/s
        if error_code != 0:
            raise RuntimeError(SGP4_ERRORS[error_code])
        
        teme_p = CartesianRepresentation(teme_p*u.km)
        teme_v = CartesianDifferential(teme_v*u.km/u.s)
        teme = TEME(teme_p.with_differentials(teme_v), obstime=current_time)

        itrs_geo =  teme.transform_to(ITRS(obstime=current_time))
        location = itrs_geo.earth_location
        location.geodetic 

        observer_x = observer['radar_x']
        observer_y = observer['radar_y']
        observer_z = observer['radar_z']

        observer_location = EarthLocation.from_geocentric(observer_x, observer_y, observer_z, unit='m')
        observer_itrs = observer_location.get_itrs(obstime=current_time)

        separation_angle = observer_itrs.separation(itrs_geo)

        print(f"Угол между наблюдателем и спутником: {separation_angle.to(u.deg):.2f} градусов")

        altaz_frame = AltAz(obstime=current_time, location=observer_location)
        satellite_altaz = itrs_geo.transform_to(altaz_frame)

        azimuth = satellite_altaz.az
        elevation = satellite_altaz.alt

        print(f"Азимут: {azimuth.to(u.deg):.2f} градусов")
        print(f"Угол места: {elevation.to(u.deg):.2f} градусов")    


        distance_value = np.sqrt((itrs_geo.x - observer_itrs.x)**2 + 
                                (itrs_geo.y - observer_itrs.y)**2 + 
                                (itrs_geo.z - observer_itrs.z)**2)
        
        distance = Distance(value=distance_value, unit = u.m)  # Преобразуем в метры

        print(f"Дальность до спутника: {distance.to(u.km):.2f} километров")

        return {
            'Azimuth': azimuth,
            'Range': distance,
            'Elevation': elevation,
        }

    
    def __del__(self):
        self.TLE_array = []
        self.satellites = []