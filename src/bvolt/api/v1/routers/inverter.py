from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from bvolt.api.v1.dependencies import get_inverter_services
from bvolt.services.inverter_service import InverterService

router = APIRouter(
    prefix="/microgrid",
    tags=["microgrid"],
)


def _resolve_inverter_service(
        inverter_id: str,
        services: list[InverterService],
) -> InverterService:
    for service in services:
        if service.inverter.asset_id == inverter_id:
            return service

    raise HTTPException(
        status_code=404,
        detail=f"Inverter '{inverter_id}' not found",
    )


@router.get("")
def list_inverters(
        services: list[InverterService] = Depends(get_inverter_services),
):
    return [
        {"inverter_id": service.inverter.asset_id}
        for service in services
    ]


@router.get("/{inverter_id}/latest")
def latest_inverter_state(
        inverter_id: str,
        services: list[InverterService] = Depends(get_inverter_services),
):
    inverter_service = _resolve_inverter_service(inverter_id, services)

    state = inverter_service.latest_state()
    return state.to_dict()


@router.get("/{inverter_id}/timeseries")
def inverter_timeseries(
        inverter_id: str,
        start: str,
        end: str,
        services: list[InverterService] = Depends(get_inverter_services),
):
    inverter_service = _resolve_inverter_service(inverter_id, services)

    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    series = inverter_service.timeseries(start, end)

    return [state.to_dict() for state in series]