from abc import ABC, abstractmethod


class PollingJob(ABC):
    """
    Abstract base class for all polling jobs.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Execute one polling cycle.
        """
        raise NotImplementedError
