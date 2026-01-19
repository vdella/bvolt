from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

# --- Primitive aliases (explicit semantics) ---

Seconds = NewType("Seconds", float)        # s
Volts = NewType("Volts", float)            # V
Amps = NewType("Amps", float)              # A
Watts = NewType("Watts", float)            # W
WattHours = NewType("WattHours", float)    # Wh
Kilowatts = NewType("Kilowatts", float)    # kW
Percent = NewType("Percent", float)        # 0..100 typically
Ratio = NewType("Ratio", float)            # 0..1 typically


# --- Helpers / conversions (explicit) ---

def clamp(value: float, low: float, high: float) -> float:
    if low > high:
        raise ValueError(f"clamp(): low={low} > high={high}")
    return max(low, min(high, value))


def kw_to_w(value_kw: float) -> float:
    return value_kw * 1000.0


def w_to_kw(value_w: float) -> float:
    return value_w / 1000.0


def wh_to_joules(value_wh: float) -> float:
    # 1 Wh = 3600 J
    return value_wh * 3600.0


def joules_to_wh(value_j: float) -> float:
    return value_j / 3600.0


# --- Value objects (optional but useful in domain) ---

@dataclass(frozen=True, slots=True)
class TimeStep:
    """Discrete simulation timestep."""
    dt_s: float

    def __post_init__(self) -> None:
        if self.dt_s <= 0:
            raise ValueError(f"TimeStep.dt_s must be > 0, got {self.dt_s}")

    @property
    def seconds(self) -> float:
        return self.dt_s


@dataclass(frozen=True, slots=True)
class Power:
    """
    Signed power convention (recommended for BVOLT domain):
    - Positive: delivery / generation (to bus)
    - Negative: consumption / absorption (from bus)
    """
    w: float

    @property
    def kw(self) -> float:
        return w_to_kw(self.w)


@dataclass(frozen=True, slots=True)
class Energy:
    """Signed energy (Wh)."""
    wh: float

    @property
    def joules(self) -> float:
        return wh_to_joules(self.wh)


@dataclass(frozen=True, slots=True)
class Voltage:
    v: float


@dataclass(frozen=True, slots=True)
class Current:
    a: float
