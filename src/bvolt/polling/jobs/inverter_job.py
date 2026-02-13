from datetime import datetime, UTC

from bvolt.polling.jobs.base import PollingJob
from bvolt.services.telemetry_service import TelemetryService
from bvolt.domain.inverter.inverter_state import InverterState
from bvolt.domain.inverter.inverter_device import Inverter
from bvolt.polling.adapters.inverter_adapter import InverterAdapter


class InverterPollingJob(PollingJob):
    """
    Polls inverter measurements and records InverterState.
    """

    def __init__(
            self,
            inverter: Inverter,
            telemetry: TelemetryService,
            adapter: InverterAdapter,
    ) -> None:
        self._inverter = inverter
        self._telemetry = telemetry
        self._adapter = adapter

    def run(self) -> None:
        state = self._inverter.state.to_dict()
        print(state)

        # self._telemetry.record_state(
        #     asset_id=self._inverter_id,
        #     state=state,
        #     timestamp=datetime.now(UTC),
        # )
        pass
