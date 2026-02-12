import minimalmodbus

from bvolt.domain.model import Device


class Inverter(Device):

    def __init__(self, address):
        super().__init__()

        self.equipment_type = f"inverter{address}"

        self.parameters = {
            "GridVoltageL1": 0,
            "GridVoltageL2": 0,
            "GridVoltageL3": 0,
            "Total_load_power": 0,
            "Battery_power": 0,
            "Sun_PV_Power": 0,
            "Emulator_PV_Power": 0,
            "Potencia_total_rede": 0,
            "Inverter_Battery_SoC": 0,
            "Inverter_Battery_Temperature": 0,
            "Inverter_Battery_voltage": 0,
            "Inverter_Battery_power": 0,
            "Inverter_Battery_current": 0,
        }

        self.instrument = minimalmodbus.Instrument("COM3", address)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.5

    ## Change temperature setpoint (SP) ##
    def change_max_pv_power(self, value):
        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.MaxSolarSellPower, value, 0
        )

    def enable_solar_sell(self, value):
        """Enable the inverter to sell PV energy production to the grid"""
        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.VendaEnergiaSolar, value, 0
        )

    def change_maximum_solar_sell_power(self, value):
        """Sets the maximum PV power to the grid"""
        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.MaxSellPower, value, 0
        )

    def change_system_work_mode(self, mode: int = 0):
        """Set the system work mode.

        0 - selling first
        1 - zero export to load
        2 - zero export to CT (current transformer)
        """
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode. Choose between 0, 1 or 2.")

        self.instrument.write_register(
            registeraddress=MODBUS_TABLE_DEYE_INVERTER.limit_control_function,
            value=mode,
        )

    def time_of_use_selling_enabled(self, days_of_the_week):
        """Set the days of the week that the time of use selling is enabled."""
        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.time_of_use_selling_enabled, days_of_the_week
        )

    def change_time_of_use_through_the_day_for(self, interval, time_of_day):
        """Set the time of day for a specific time of use interval.
        Must be a time between 0 and 2359 (as 23:59, the end of the day)."""

        if time_of_day < 0 or time_of_day > 2400:
            raise ValueError("Invalid time of day. Choose between 0 and 2400.")

        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.time_of_use_through_the_day[interval],
            time_of_day,
        )

    def change_time_of_use_battery_output_power_for(self, interval, power):
        """Set the power output for a specific time of use interval.
        Must be a power between 0 and 8000 W."""

        if power < 0 or power > 8000:
            raise ValueError("Invalid power. Choose between 0 and 10000.")

        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.time_of_use_battery_output_power[interval], power
        )

    def change_battery_capacity_through_the_day_for(self, interval, capacity):
        """Set the battery capacity for a specific time of use interval.
        Must be a capacity between 0 and 100%."""

        if capacity < 0 or capacity > 100:
            raise ValueError("Invalid capacity. Choose between 0 and 100.")

        self.instrument.write_register(
            MODBUS_TABLE_DEYE_INVERTER.battery_capacity_through_the_day[interval],
            capacity,
        )

    @staticmethod
    def digest_temperature_reading(temperature_from_manual):
        """Retrieves the battery bank temperature as stated from the manual and digests it
        to a more human-readable format.

        If the reading is 1000, the actual temperature is 0ºC.
        If it is 1200, the actual temperature is 20ºC.
        If it is 800, the actual temperature is -20ºC.
        """

        actual_temp = temperature_from_manual - 1000
        actual_temp /= 10

        return actual_temp

    def read_register(
            self, register, decimals, function=3, signed=False, max_retries=5
    ):
        return super().read_register(register, decimals, function, signed)

    @error("Failed to read DEYE inverter registers.")
    def update_readings(self):
        self.parameters["GridVoltageL1"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.gridVoltageL1, 1, 3
        )

        self.parameters["GridVoltageL2"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.gridVoltageL2, 1, 3
        )

        self.parameters["GridVoltageL3"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.gridVoltageL3, 1, 3
        )

        self.parameters["Total_load_power"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.Total_load_power, 0, 3
        )

        self.parameters["Sun_PV_Power"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.pv1Power, 0, 3
        )

        self.parameters["Emulator_PV_Power"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.pv2Power, 0, 3
        )

        self.parameters["Potencia_total_rede"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.Potencia_total_rede, 0, 3, signed=True
        )

        temperature_from_register = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.battery1_temperature, 0, 3
        )
        self.parameters["Inverter_Battery_Temperature"] = self.digest_temperature_reading(
            temperature_from_register
        )

        self.parameters["Inverter_Battery_SoC"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.SoC, 0, 3
        )

        self.parameters["Inverter_Battery_voltage"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.Battery_voltage, 2, 3
        )

        self.parameters["Inverter_Battery_power"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.Battery_power, 0, 3, signed=True
        )

        self.parameters["Inverter_Battery_current"] = self.read_register(
            MODBUS_TABLE_DEYE_INVERTER.Battery_current, 2, 3, signed=True
        )

    def write_to_db(self):
        return super().write_to_db()


if __name__ == "__main__":
    inv1 = Inverter(1)
    inv1.instrument.close_port_after_each_call = True

    inv2 = Inverter(2)
    inv2.instrument.close_port_after_each_call = True

    inv1.update_readings()
    print(inv1.equipment_type)
    print(inv1.parameters)

    inv2.update_readings()
    print(inv2.equipment_type)
    print(inv2.parameters)