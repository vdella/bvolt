from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from bvolt.api.v1.dependencies import get_battery_services
from bvolt.services.battery_service import BatteryService

router = APIRouter(
    prefix="/battery",
    tags=["battery"],
)


def _resolve_battery_service(
        battery_id: str,
        services: list[BatteryService],
) -> BatteryService:
    for service in services:
        if service.battery.asset_id == battery_id:
            return service

    raise HTTPException(
        status_code=404,
        detail=f"Battery '{battery_id}' not found",
    )


@router.get("")
def list_batteries(
        services: list[BatteryService] = Depends(get_battery_services),
):
    return [
        {"battery_id": service.battery.asset_id}
        for service in services
    ]


@router.get("/{battery_id}/latest")
def latest_battery_state(
        battery_id: str,
        services: list[BatteryService] = Depends(get_battery_services),
):
    """
    Return the latest known state for a specific battery.
    """
    battery_service = _resolve_battery_service(battery_id, services)

    state = battery_service.latest_state()
    return state.to_dict()


@router.get("/{battery_id}/timeseries")
def battery_timeseries(
        battery_id: str,
        start: str,
        end: str,
        services: list[BatteryService] = Depends(get_battery_services),
):
    """
    Return the battery timeseries over a given time range.
    """
    battery_service = _resolve_battery_service(battery_id, services)

    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    series = battery_service.timeseries(start, end)

    return [state.to_dict() for state in series]