from datetime import datetime, UTC

from bvolt.polling.jobs.base import PollingJob
from bvolt.services.telemetry_service import TelemetryService
from bvolt.domain.state import State


class BatteryPollingJob(PollingJob):
    """
    Polls battery measurements and records state.
    """

    def __init__(
            self,
            battery_id: str,
            telemetry: TelemetryService,
    ) -> None:
        self._battery_id = battery_id
        self._telemetry = telemetry

    def run(self) -> None:
        # TODO: replace with real adapter reads
        state = State()  # placeholder domain object

        self._telemetry.record_state(
            asset_id=self._battery_id,
            state=state,
            timestamp=datetime.now(UTC),
        )
