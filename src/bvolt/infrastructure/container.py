from bvolt.services.telemetry_service import TelemetryService
from bvolt.services.battery_service import BatteryService
from bvolt.services.microgrid_service import MicrogridService


def build_telemetry_service() -> TelemetryService:
    """
    Construct the TelemetryService with the appropriate reader/writer.
    """
    raise NotImplementedError


def build_battery_services() -> list[BatteryService]:
    """
    Construct BatteryService instances for all configured batteries.
    """
    raise NotImplementedError


def build_microgrid_service() -> MicrogridService:
    """
    Construct the MicrogridService from all asset services.
    """
    raise NotImplementedError
