import minimalmodbus
import random

from bvolt.domain.device import Device
from bvolt.domain.inverter.inverter_state import InverterState


class Inverter(Device):

    def __init__(self, address):
        super().__init__()

        self.label = f"inverter_{address}"

        self.state = {
            "grid_voltage_l1": random.uniform(40.0, 80.0),
            "grid_voltage_l2": random.uniform(48.0, 54.0),
            "grid_voltage_l3": random.uniform(-20.0, 20.0),

            "pv_power": random.uniform(40.0, 80.0),

            "battery_soc": random.uniform(40.0, 80.0),
            "battery_voltage": random.uniform(40.0, 80.0),
            "battery_current": random.uniform(40.0, 80.0),
            "battery_power": random.uniform(40.0, 80.0),
            "battery_temperature": random.uniform(40.0, 80.0),
        }

        # self.instrument = minimalmodbus.Instrument("COM3", address)
        # self.instrument.serial.baudrate = 9600
        # self.instrument.serial.timeout = 0.5

    def read_register(
            self, register, decimals, function=3, signed=False, max_retries=5
    ):
        raise NotImplementedError

    def write_register(self, register, value, decimals, function, signed):
        raise NotImplementedError