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

    def to_dict(self) -> Dict[str, float]:
        return {
            "grid_voltage_l1": self.grid_voltage_l1,
            "grid_voltage_l2": self.grid_voltage_l2,
            "grid-voltage_l3": self.grid_voltage_l3,
        }