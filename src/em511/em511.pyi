from decimal import Decimal

from pymodbus.client import ModbusSerialClient

class Em511:
    def __init__(self, device_address: int, client: ModbusSerialClient) -> None: ...
    V: Decimal
    A: Decimal
    password: int
