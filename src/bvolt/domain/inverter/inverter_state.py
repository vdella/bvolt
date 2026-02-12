from dataclasses import dataclass
from typing import Dict

from bvolt.domain.state import State


@dataclass(frozen=True)
class InverterState(State):
    """
    Immutable snapshot of an inverter state.
    """

    grid_voltage_l1: float
    grid_voltage_l2: float
    grid_voltage_l3: float

    pv_power: float

    battery_soc: float
    battery_voltage: float
    battery_current: float
    battery_power: float
    battery_temperature: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "grid_voltage_l1": self.grid_voltage_l1,
            "grid_voltage_l2": self.grid_voltage_l2,
            "grid-voltage_l3": self.grid_voltage_l3,

            "pv_power": self.pv_power,

            "battery_soc": self.battery_soc,
            "battery_voltage": self.battery_voltage,
            "battery_current": self.battery_current,
            "battery_power": self.battery_power,
            "battery_temperature": self.battery_temperature,
        }