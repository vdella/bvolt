from fastapi import APIRouter, Depends
from datetime import datetime

from bvolt.api.v1.dependencies import get_microgrid_service
from bvolt.services.microgrid_service import MicrogridService

router = APIRouter(
    prefix="/microgrid",
    tags=["microgrid"],
)

@router.get("/snapshot")
def system_snapshot(
        microgrid_service: MicrogridService = Depends(get_microgrid_service),
):
    snapshot = microgrid_service.system_snapshot()

    return {
        "batteries": [
            state.to_dict()
            for state in snapshot
        ]
    }


@router.get("/timeseries")
def microgrid_timeseries(
        start: str,
        end: str,
        microgrid_service: MicrogridService = Depends(get_microgrid_service),
):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    return microgrid_service.timeseries(start=start, end=end)


@router.get("/operating-mode")
def operating_mode(
        microgrid_service: MicrogridService = Depends(get_microgrid_service),
):
    mode = microgrid_service.operating_mode()
    return {"operating_mode": mode}