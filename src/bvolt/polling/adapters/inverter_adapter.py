import random


class InverterAdapter:
    """
    Temporary adapter for battery measurements.
    Replace with Modbus/Serial later.
    """

    @staticmethod
    def read() -> dict:
        return {
            "grid_voltage_l1": random.uniform(40.0, 80.0),
            "grid_voltage_l2": random.uniform(48.0, 54.0),
            "grid_voltage_l3": random.uniform(-20.0, 20.0),
        }
