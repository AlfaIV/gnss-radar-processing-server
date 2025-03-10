from pydantic import BaseModel
from typing import List

class RadarPosition(BaseModel):
    RadarX: int
    RadarY: int
    RadarZ: int
    RadarID: int

class SatellitePosition(BaseModel):
    Name: str
    Azimuth: int
    Range: int

class SatellitesPosition(BaseModel):
    Satellites: List[SatellitePosition]