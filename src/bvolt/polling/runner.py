class PollingRunner:
    """
    Coordinates execution of polling jobs.
    """

    def __init__(self, jobs):
        self._jobs = jobs

    def start(self) -> None:
        """
        Start the polling runner.
        """
        raise NotImplementedError

    def stop(self) -> None:
        """
        Stop the polling runner.
        """
        raise NotImplementedError