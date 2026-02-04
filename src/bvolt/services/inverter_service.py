from typing import Iterable
from datetime import datetime

from bvolt.domain.state import State
from bvolt.domain.inverter import Inverter
from bvolt.services.telemetry_service import TelemetryService

class InverterService:
    """
    Application-level service for providing interface
    with physical inverter asset objects.

    This service is the union between EMS intent
    and the physical inverter in the plant. It checks
    and enforces models, states and constraints.
    """

    def __init__(self, inverter: Inverter, telemetry: TelemetryService) -> None:
        """
        Initialize the InverterService.

        Parameters
        ----------
        inverter:
            Inverter asset object, carrying model, states and
            constraints.
        telemetry:
            TelemetryService for reading and writing inverter-related data.
        """
        self.inverter = inverter
        self._telemetry = telemetry

    def latest_state(self) -> State:
        """
        Retrieve the most recent recorded state for an inverter asset.

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
        an inverter asset over a specified time range.
        """
        raise NotImplementedError