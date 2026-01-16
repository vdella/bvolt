from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class BatteryState:
    """
    Immutable snapshot of a battery state.
    """

    soc: float  # Interval between [0–100]
    voltage: float  # Volts
    current: float  # Amperes
    power: float # Watts
    temperature: float  # °C

    def __post_init__(self) -> None:
        if not 0.0 <= self.soc <= 100.0:
            raise ValueError("SOC must be between 0 and 100")

        if self.voltage <= 0.0:
            raise ValueError("Voltage must be positive")

    def to_dict(self) -> Dict[str, float]:
        return {
            "soc": self.soc,
            "voltage": self.voltage,
            "current": self.current,
            "power": self.power,
            "temperature": self.temperature,
        }