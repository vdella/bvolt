from datetime import datetime, UTC

from bvolt.polling.jobs.base import PollingJob
from bvolt.services.telemetry_service import TelemetryService
from bvolt.domain.battery.state import BatteryState
from bvolt.polling.adapters.battery_adapter import BatteryAdapter


class BatteryPollingJob(PollingJob):
    """
    Polls battery measurements and records BatteryState.
    """

    def __init__(
            self,
            battery_id: str,
            telemetry: TelemetryService,
            adapter: BatteryAdapter,
    ) -> None:
        self._battery_id = battery_id
        self._telemetry = telemetry
        self._adapter = adapter

    def run(self) -> None:
        raw = self._adapter.read()

        power = raw["voltage"] * raw["current"]

        state = BatteryState(
            soc=raw["soc"],
            voltage=raw["voltage"],
            current=raw["current"],
            power=power,
            temperature=raw.get("temperature"),
        )

        self._telemetry.record_state(
            asset_id=self._battery_id,
            state=state,
            timestamp=datetime.now(UTC),
        )
