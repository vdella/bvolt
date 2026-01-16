import random


class BatteryAdapter:
    """
    Temporary adapter for battery measurements.
    Replace with Modbus/Serial later.
    """

    def read(self) -> dict:
        return {
            "soc": random.uniform(40.0, 80.0),
            "voltage": random.uniform(48.0, 54.0),
            "current": random.uniform(-20.0, 20.0),
            "temperature": random.uniform(20.0, 35.0),
        }
