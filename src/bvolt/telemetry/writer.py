from abc import ABC, abstractmethod
from datetime import datetime
from bvolt.domain.state import State


class TelemetryWriter(ABC):
    """
    Defines how domain state snapshots are written to telemetry storage.
    """

    @abstractmethod
    def record_state(
            self,
            asset_id: str,
            state: State,
            timestamp: datetime,
    ) -> None:
        """
        Persist a snapshot of a State associated with a given asset.
        """
        raise NotImplementedError
