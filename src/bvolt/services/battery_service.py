from typing import Iterable
from datetime import datetime

from bvolt.domain.state import State
from bvolt.domain.battery import Battery
from bvolt.services.telemetry_service import TelemetryService

class BatteryService:
    """
    Application-level service for providing interface
    with physical battery asset objects.

    This service is the union between EMS intent
    and the physical battery in the plant. It checks
    and enforces models, states and constraints.
    """

    def __init__(self, battery: Battery, telemetry: TelemetryService) -> None:
        """
        Initialize the BatteryService.

        Parameters
        ----------
        battery:
            Battery asset object, carrying model, states and
            constraints.
        telemetry:
            TelemetryService for reading and writing battery-related data.
        """
        self.battery = battery
        self._telemetry = telemetry

    def latest_state(self) -> State:
        """
        Retrieve the most recent recorded state for a battery asset.

        This method does not guarantee real-time data. It returns the
        last known telemetry snapshot.
        """
        raise NotImplementedError

    def timeseries(
            self,
            start: datetime,
            end: datetime,
    ) -> Iterable[State]:
        """
        Retrieve an ordered sequence of historical state snapshots for
        a battery asset over a specified time range.
        """
        raise NotImplementedError