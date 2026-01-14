class ApplicationLifecycle:
    """
    Handles application startup and shutdown.
    """

    def start(self) -> None:
        """
        Start application resources.
        """
        raise NotImplementedError

    def stop(self) -> None:
        """
        Stop application resources.
        """
        raise NotImplementedError
