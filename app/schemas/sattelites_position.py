from pydantic import BaseModel
from typing import List, Union

class RadarPositionRequest(BaseModel):
    radar_x: int
    radar_y: int
    radar_z: int

class SatellitePosition(BaseModel):
    Name: str
    Azimuth: int
    Range: int

class SatellitesPositionResponce(BaseModel):
    Satellites: List[SatellitePosition]