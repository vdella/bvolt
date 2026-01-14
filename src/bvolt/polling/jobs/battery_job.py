from bvolt.services.battery_service import BatteryService


class BatteryPollingJob:
    """
    Polling job responsible for acquiring battery measurements
    and producing BatteryState snapshots.
    """

    def __init__(self, adapter, battery_service: BatteryService) -> None:
        self._adapter = adapter
        self._battery_service = battery_service

    def poll(self) -> None:
        """
        Perform a single polling cycle.
        """
        raise NotImplementedError
