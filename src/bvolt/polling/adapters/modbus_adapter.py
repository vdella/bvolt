class ModbusAdapter:
    """
    Adapter for communicating with Modbus-capable devices.
    """

    def read(self):
        """
        Read raw values from the device.
        """
        raise NotImplementedError
