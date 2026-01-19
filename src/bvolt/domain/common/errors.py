from __future__ import annotations


class DomainError(Exception):
    """Base class for all BVOLT domain errors."""


class ValidationError(DomainError):
    """Raised when a domain object or input violates basic validation rules."""


class InvariantViolation(DomainError):
    """Raised when a domain invariant is broken (indicates a bug or invalid state transition)."""


class ConstraintViolation(DomainError):
    """Raised when a requested operation violates a physical/operational constraint."""


class UnsupportedOperation(DomainError):
    """Raised when an operation is not supported by the current model/configuration."""


class NotFound(DomainError):
    """Raised when a requested domain entity cannot be found (primarily for in-memory domain registries)."""


class TimeError(DomainError):
    """Raised when there is an invalid time-step or temporal inconsistency."""
