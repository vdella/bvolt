import minimalmodbus

from abc import ABC, abstractmethod

from minimalmodbus import Instrument

from bvolt.domain.state import State


class Device(ABC):

    equipment_type: str
    instrument: "Instrument"

    state: State

    @abstractmethod
    def read_register(self, register, decimals, function, signed):
        raise NotImplementedError

    @abstractmethod
    def write_register(self, register, value, decimals, function, signed):
        raise NotImplementedError
