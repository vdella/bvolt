from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generic, Mapping, Optional, Protocol, TypeVar, runtime_checkable

from errors import TimeError, ValidationError


# -------------------------
# Core DDD-like primitives
# -------------------------

@dataclass(frozen=True, slots=True)
class EntityId:
    """Stable identifier for domain entities."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValidationError("EntityId.value must be a non-empty string")


@dataclass(frozen=True, slots=True)
class Entity:
    """Base identifiable domain object."""
    id: EntityId
    name: str = ""

    def __post_init__(self) -> None:
        if self.name and not self.name.strip():
            raise ValidationError("Entity.name cannot be only whitespace")


@dataclass(frozen=True, slots=True)
class ValueObject:
    """
    Marker base for value objects.
    Dataclasses inheriting from this are expected to be immutable and comparable by value.
    """


# -------------------------
# Snapshots (domain-facing)
# -------------------------

@dataclass(frozen=True, slots=True)
class Snapshot(ValueObject):
    """
    A lightweight, serializable view of a domain object's state.
    Intended for logging, testing, and adapters (telemetry publishing),
    without coupling the domain to specific schemas.
    """
    data: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)


# -------------------------
# Time evolution protocol
# -------------------------

@runtime_checkable
class Stepable(Protocol):
    def step(self, dt: float) -> None:
        """
        Advance internal state by dt seconds.
        Must be deterministic and side-effect free w.r.t. external systems.
        """


S = TypeVar("S", bound=Snapshot)


class Asset(Entity, Generic[S]):
    """
    Base class for a stateful asset in a microgrid digital twin.

    Assets evolve in time with `step(dt)` and expose their current state via `snapshot()`.
    """
    nominal_power_w: Optional[float] = None

    def validate_dt(self, dt: float) -> None:
        if dt is None:
            raise TimeError("dt cannot be None")
        try:
            dt_f = float(dt)
        except (TypeError, ValueError) as exc:
            raise TimeError(f"dt must be a float-like value, got {dt!r}") from exc
        if dt_f <= 0.0:
            raise TimeError(f"dt must be > 0, got {dt_f}")

    def step(self, dt: float) -> None:
        """
        Default step does nothing (useful for static assets).
        Override in subclasses to implement physics/logic.
        """
        self.validate_dt(dt)

    def snapshot(self) -> S:
        """
        Return an immutable snapshot of the asset's state.
        Subclasses should override to provide domain-meaningful fields.
        """
        base = {
            "id": self.id.value,
            "name": self.name,
            "nominal_power_w": self.nominal_power_w,
            "type": self.__class__.__name__,
        }
        return Snapshot(base)  # type: ignore[return-value]