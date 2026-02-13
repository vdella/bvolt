from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from bvolt.domain.inverter.inverter_device import Inverter
from bvolt.api.v1.dependencies import get_inverter_services
from bvolt.services.inverter_service import InverterService

router = APIRouter(
    prefix="/inverter",
    tags=["inverter"],
)

services = get_inverter_services()

@router.get("")
def latest_state():
    return {
        "inverter_1": services["inverter_1"].latest_state(),
        "inverter_2": services["inverter_2"].latest_state(),
    }


@router.get("/timeseries")
def timeseries(
        start: str,
        end: str
):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)

    inverter_1_series = services["inverter_1"].timeseries(start, end)
    inverter_2_series = services["inverter_2"].timeseries(start, end)

    return {
        "inverter_1": [state.to_dict() for state in inverter_1_series],
        "inverter_2": [state.to_dict() for state in inverter_2_series],
    }