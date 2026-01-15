"""
FastAPI call dependencies per request, so, in order to get singleton-like
behavior, @lru_cache needs to be called for routers.
"""
from functools import lru_cache

from bvolt.services.battery_service import BatteryService
from bvolt.services.microgrid_service import MicrogridService
from bvolt.infrastructure.container import (
    build_microgrid_service,
    build_battery_services,
)


@lru_cache
def get_battery_service(asset_id) -> list[BatteryService]:
    return build_battery_services(asset_id)


@lru_cache
def get_microgrid_service(asset_id) -> MicrogridService:
    return build_microgrid_service(asset_id)