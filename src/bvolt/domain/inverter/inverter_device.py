import minimalmodbus

from bvolt.domain.device import Device
from bvolt.domain.inverter.inverter_state import InverterState


class Inverter(Device):

    def __init__(self, address):
        super().__init__()

        self.label = f"inverter_{address}"

        self.state: list[InverterState] = []

        self.instrument = minimalmodbus.Instrument("COM3", address)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.5

    def read_register(
            self, register, decimals, function=3, signed=False, max_retries=5
    ):
        raise NotImplementedError

    def write_register(self, register, value, decimals, function, signed):
        raise NotImplementedError