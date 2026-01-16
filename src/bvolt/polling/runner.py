import time
from typing import Iterable

from bvolt.polling.jobs.base import PollingJob


class PollingRunner:
    """
    Coordinates execution of polling jobs.
    """

    def __init__(
            self,
            jobs: Iterable[PollingJob],
            interval_seconds: float,
    ) -> None:
        self._jobs = jobs
        self._interval = interval_seconds
        self._running = False

    def start(self) -> None:
        self._running = True

        while self._running:
            for job in self._jobs:
                job.run()

            time.sleep(self._interval)

    def stop(self) -> None:
        self._running = False
