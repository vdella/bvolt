from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from bvolt.api.v1.dependencies import get_battery_service
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
        services: list[BatteryService] = Depends(get_battery_service),
):
    return [
        {"battery_id": service.battery.asset_id}
        for service in services
    ]


@router.get("/{battery_id}/latest")
def latest_battery_state(
        battery_id: str,
        services: list[BatteryService] = Depends(get_battery_service),
):
    """
    Return the latest known state for a specific battery.
    """
    battery_service = _resolve_battery_service(battery_id, services)

    try:
        return battery_service.latest_state()
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Battery state not implemented yet",
        )


@router.get("/{battery_id}/timeseries")
def battery_timeseries(
        battery_id: str,
        start: str,
        end: str,
        services: list[BatteryService] = Depends(get_battery_service),
):
    """
    Return the battery timeseries over a given time range.
    """
    battery_service = _resolve_battery_service(battery_id, services)

    try:
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)
        return battery_service.timeseries(start=start, end=end)
    except NotImplementedError:
        raise HTTPException(
            status_code=501,
            detail="Battery timeseries not implemented yet",
        )