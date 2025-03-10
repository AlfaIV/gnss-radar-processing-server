from pydantic import BaseModel
from typing import List, Union

class RadarPositionRequest(BaseModel):
    radar_x: int
    radar_y: int
    radar_z: int

class SatellitePosition(BaseModel):
    Group: str
    Name: str
    Azimuth: float
    Range: float

class SatellitesPositionResponce(BaseModel):
    Satellites: List[SatellitePosition]