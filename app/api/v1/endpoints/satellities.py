
from fastapi import APIRouter, Depends

from app.schemas.sattelites_position import RadarPosition, SatellitesPosition

router = APIRouter(
    prefix="/satellites",
    tags=["auth"],
)

@router.get('/now', response_model=SatellitesPosition)
def get_sattelites():
    return {
        'Satellites': [
            {
                'Name': '123',
                'Azimuth': 10,
                'Range': 10,
            }
        ]
    }