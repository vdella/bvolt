from typing import Iterable
from datetime import datetime

from bvolt.domain.state import State
from bvolt.services.battery_service import BatteryService
from bvolt.services.telemetry_service import TelemetryService

class MicrogridService:
    """
    Application-level service for operating the microgrid.

    This is the core service of EMS, and encapsulates all
    known asset-related services.
    """

    def __init__(self, batteries: Iterable[BatteryService], telemetry: TelemetryService) -> None:
        """
        Initialize the MicrogridService.

        Parameters
        ----------
        batteries:
            BatteryService iterables for all available batteries.
        telemetry:
            TelemetryService for reading and writing assets-related data.
        """
        self._batteries = batteries
        self._telemetry = telemetry

    def system_snapshot(self) -> Iterable[State]:
        """
        Retrieve the most recent recorded states for all physical and logical microgrid
        assets.

        This method does not guarantee real-time data. It returns the
        last known system telemetry snapshot.
        """
        raise NotImplementedError

    def timeseries(
            self,
            start: datetime,
            end: datetime,
    ) -> Iterable[Iterable[State]]:
        """
        Retrieve ordered sequences of historical state snapshots for
        a all physical and logical asset over a specified time range.
        """
        raise NotImplementedError

    def record_state(
            self,
            state: State,
            timestamp: datetime,
    ) -> None:
        """
        Persist a snapshot of domain state for all assets.

        This operation is intended for trusted internal processes such
        as the polling runtime or EMS services.
        """
        raise NotImplementedError

    def operating_mode(self) -> None:
        """
        Infer microgrid operating mode from observing all physical and
        logical assets operations.
        """
        raise NotImplementedError