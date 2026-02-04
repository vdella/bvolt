from bvolt.polling.adapters.battery_adapter import BatteryAdapter
from bvolt.polling.adapters.inverter_adapter import InverterAdapter
from bvolt.polling.runner import PollingRunner
from bvolt.polling.jobs.battery_job import BatteryPollingJob
from bvolt.infrastructure.container import build_telemetry_service


class ApplicationLifecycle:
    """
    Handles application startup and shutdown.
    """

    def __init__(self):
        telemetry = build_telemetry_service()

        jobs = [
            BatteryPollingJob(
                battery_id="battery_id",  # TODO change so it comports multiple batteries.
                telemetry=telemetry,
                adapter=BatteryAdapter()
            ),

            InverterPollingJob(
                inverter_id="inverter_id",  # TODO change so it comports multiple inverters.
                telemetry=telemetry,
                adapter=InverterAdapter()
            )
        ]

        self._runner = PollingRunner(jobs=jobs, interval_seconds=0.5)  # Arbitrary number of seconds.

    def start(self) -> None:
        """
        Start application resources.
        """
        self._runner.start()

    def stop(self) -> None:
        """
        Stop application resources.
        """
        self._runner.stop()
