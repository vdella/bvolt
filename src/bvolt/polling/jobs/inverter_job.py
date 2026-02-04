from datetime import datetime, UTC

from bvolt.polling.jobs.base import PollingJob
from bvolt.services.telemetry_service import TelemetryService
from bvolt.domain.inverter.state import InverterState
from bvolt.polling.adapters.inverter_adapter import InverterAdapter


class InverterPollingJob(PollingJob):
    """
    Polls inverter measurements and records InverterState.
    """

    def __init__(
            self,
            inverter_id: str,
            telemetry: TelemetryService,
            adapter: InverterAdapter,
    ) -> None:
        self._inverter_id = inverter_id
        self._telemetry = telemetry
        self._adapter = adapter

    def run(self) -> None:
        raw = self._adapter.read()

        state = InverterState(
            grid_voltage_l1=raw["grid_voltage_l1"],
            grid_voltage_l2=raw["grid_voltage_l2"],
            grid_voltage_l3=raw["grid_voltage_l3"],
        )

        self._telemetry.record_state(
            asset_id=self._inverter_id,
            state=state,
            timestamp=datetime.now(UTC),
        )
