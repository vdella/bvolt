from abc import ABC, abstractmethod
from typing import Dict


class State(ABC):
    """
    Abstract base class for all domain state snapshots.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, float]:
        """
        Serialize state to a flat dictionary for telemetry.
        """
        raise NotImplementedError
