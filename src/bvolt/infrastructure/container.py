from bvolt.domain.battery.model import Battery
from bvolt.services.telemetry_service import TelemetryService
from bvolt.services.battery_service import BatteryService
from bvolt.services.microgrid_service import MicrogridService
from bvolt.telemetry.influx_adapter import InfluxTelemetryReader, InfluxTelemetryWriter


def build_telemetry_service() -> TelemetryService:
    """
    Construct the TelemetryService with the appropriate reader/writer.
    """
    telemetry_reader = InfluxTelemetryReader()
    telemetry_writer = InfluxTelemetryWriter()
    return TelemetryService(telemetry_reader, telemetry_writer)


def build_battery_services(battery_id: str) -> list[BatteryService]:
    # TODO: load battery definitions from config
    battery = Battery(asset_id=battery_id)
    telemetry = build_telemetry_service()

    return [
        BatteryService(
            battery=battery,
            telemetry=telemetry,
        )
    ]


def build_microgrid_service(asset_id) -> MicrogridService:
    batteries = build_battery_services(asset_id)
    telemetry = build_telemetry_service()

    return MicrogridService(
        batteries=batteries,
        telemetry=telemetry,
    )
