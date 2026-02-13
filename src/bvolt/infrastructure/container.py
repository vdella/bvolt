from typing import Dict

from bvolt.services.inverter_service import InverterService
from bvolt.services.telemetry_service import TelemetryService
from bvolt.telemetry.influx_adapter import InfluxTelemetryReader, InfluxTelemetryWriter
from bvolt.domain.inverter.inverter_device import Inverter


def build_telemetry_service() -> TelemetryService:
    """
    Construct the TelemetryService with the appropriate reader/writer.
    """
    telemetry_reader = InfluxTelemetryReader()
    telemetry_writer = InfluxTelemetryWriter()
    return TelemetryService(telemetry_reader, telemetry_writer)


def build_inverter_services() -> Dict[str, InverterService]:
    inverter_1 = Inverter(1)
    inverter_2 = Inverter(2)

    telemetry = build_telemetry_service()

    inverter_1_service = InverterService(
        inverter=inverter_1,
        telemetry=telemetry,
    )

    inverter_2_service = InverterService(
        inverter=inverter_2,
        telemetry=telemetry
    )

    return {
        'inverter_1': inverter_1_service,
        'inverter_2': inverter_2_service,
    }