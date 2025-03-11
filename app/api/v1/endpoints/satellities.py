from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container
from app.services.sattelites_positions import SatellitesPositions
from app.schemas.sattelites_position import RadarPositionRequest, SatellitesPositionResponce

router = APIRouter(
    prefix="/satellites",
    tags=["satellites"],
)

@router.post('/now', response_model=SatellitesPositionResponce)
@inject
def post_sattelites(
    radar: RadarPositionRequest,
    service: SatellitesPositions = Depends(Provide[Container.satellite_services]),
):
    return service.get_sattelites_positions(radar)