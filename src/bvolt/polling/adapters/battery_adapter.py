import random


class BatteryBankAdapter:
    """
    Temporary adapter for battery measurements.
    Replace with Modbus/Serial later.
    """

    @staticmethod
    def read() -> dict:
        return {
            "soc": random.uniform(40.0, 80.0),
            "voltage": random.uniform(48.0, 54.0),
            "current": random.uniform(-20.0, 20.0),
            "temperature": random.uniform(20.0, 35.0),
        }
