from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime
from bvolt.domain.state import State


class TelemetryReader(ABC):
    """
    Defines how domain state is read from telemetry storage.
    """

    @abstractmethod
    def read_latest_state(self, asset_id: str) -> State:
        """
        Return the most recent recorded State for the given asset.
        """
        raise NotImplementedError

    @abstractmethod
    def read_timeseries(
            self,
            asset_id: str,
            start: datetime,
            end: datetime,
    ) -> Iterable[State]:
        """
        Return an ordered sequence of State snapshots for a given
        asset over a specified time range.
        """
        raise NotImplementedError
