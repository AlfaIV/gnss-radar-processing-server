
from fastapi import APIRouter, Depends
from typing import List

from app.services.sattelites_positions import SatellitesPositions
from app.schemas.sattelites_position import RadarPositionRequest, SatellitesPositionResponce

router = APIRouter(
    prefix="/satellites",
    tags=["auth"],
)

@router.post('/now', response_model=SatellitesPositionResponce)
def post_sattelites(radar: RadarPositionRequest):
    service = SatellitesPositions()
    return service.get_sattelites_positions(radar)
    # return {'Satellites': []}
    # return {
    #     'Satellites': [
    #         {
    #             'Name': '123',
    #             'Azimuth': 10,
    #             'Range': 10,
    #         }
    #     ]
    # }