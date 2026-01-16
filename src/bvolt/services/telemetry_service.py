from typing import Iterable
from datetime import datetime

from bvolt.domain.state import State
from bvolt.telemetry.reader import TelemetryReader
from bvolt.telemetry.writer import TelemetryWriter


class TelemetryService:
    """
    Application-level service that provides access to telemetry data.

    This service acts as the official boundary through which the EMS
    interacts with telemetry. It orchestrates read/write access to
    domain state without exposing storage or backend details.
    """

    def __init__(
            self,
            reader: TelemetryReader,
            writer: TelemetryWriter,
    ) -> None:
        """
        Initialize the TelemetryService.

        Parameters
        ----------
        reader:
            TelemetryReader implementation used for reading domain state.
        writer:
            Optional TelemetryWriter implementation used for persisting
            domain state snapshots. May be None if the runtime is read-only.
        """
        self._reader = reader
        self._writer = writer

    def latest_state(self, asset_id: str) -> State:
        """
        Retrieve the most recent recorded state for a given asset.

        This method does not guarantee real-time data. It returns the
        last known telemetry snapshot.
        """
        return self._reader.latest_state(asset_id)

    def timeseries(
            self,
            asset_id: str,
            start: datetime,
            end: datetime,
    ) -> Iterable[State]:
        """
        Retrieve an ordered sequence of historical state snapshots for
        a given asset over a specified time range.
        """
        return self._reader.timeseries(asset_id, start, end)

    def record_state(
            self,
            asset_id: str,
            state: State,
            timestamp: datetime,
    ) -> None:
        """
        Persist a snapshot of domain state for a given asset.

        This operation is intended for trusted internal processes such
        as the polling runtime or EMS services.
        """
        return self._writer.record_state(asset_id, state, timestamp)