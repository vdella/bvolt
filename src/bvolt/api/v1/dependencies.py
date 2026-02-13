"""
FastAPI call dependencies per request, so, in order to get singleton-like
behavior, @lru_cache needs to be called for routers.
"""
from functools import lru_cache
from typing import Dict

from bvolt.services.inverter_service import InverterService
from bvolt.infrastructure.container import build_inverter_services


@lru_cache
def get_inverter_services() -> Dict[str, InverterService]:
    return build_inverter_services()