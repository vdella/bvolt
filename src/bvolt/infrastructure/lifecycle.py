from bvolt.domain.inverter.inverter_device import Inverter
from bvolt.polling.adapters.inverter_adapter import InverterAdapter
from bvolt.polling.runner import PollingRunner
from bvolt.infrastructure.container import build_telemetry_service
from bvolt.polling.jobs.inverter_job import InverterPollingJob


class ApplicationLifecycle:
    """
    Handles application startup and shutdown.
    """

    def __init__(self):
        telemetry = build_telemetry_service()

        inverter_1 = Inverter(1)
        inverter_2 = Inverter(2)

        jobs = [
            InverterPollingJob(
                inverter=inverter_1,
                telemetry=telemetry,
                adapter=InverterAdapter()
            ),

            InverterPollingJob(
                inverter=inverter_2,
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
