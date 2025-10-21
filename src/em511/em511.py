"""Driver class for EM511."""

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException


class Em511:
    """Driver for Carlo Gavazzi EM511 series energy meters.

    This class provides read and write access to Modbus registers
    via a connected `pymodbus.client.ModbusSerialClient` instance.

    Attributes:
        device_address (int): Modbus address of the target device.
        client (ModbusSerialClient): Connected Modbus client.
        connected (bool): True if connection is established.
    """

    INT16_REG_COUNT = 1
    INT32_REG_COUNT = 2

    def __init__(self, device_address: int, client: ModbusSerialClient) -> None:
        """Initialize an Em511 driver instance.

        Sets up Modbus communication with the specified device address.

        Args:
            device_address: Modbus address for the EM511 meter.
            client: ModbusSerialClient instance used for communication.
        """
        self.device_address = device_address
        self.client = client

    def _read_input_registers(self, address: int, count: int) -> list[int]:
        """Read input registers.

        Internal helper to read Modbus registers safely.

        Args:
            address: Register adress to read from.
            count: Number of register to read from

        Returns:
            value of registers.
        """
        result = self.client.read_input_registers(address=address, count=count, device_id=self.device_address)
        if result.isError():
            msg = f"Failed to read input register. result={result} "
            f"device_address={self.device_address} address={address} count={count}"
            raise ModbusException(msg)
        return result.registers

    def _write_register(self, address: int, value: int) -> None:
        """Write to register.

        Internal helper to write to single register.

        Args:
            address: Register to write to.
            value: Value to write the given register with.

        Returns:
            True if register was written to.
        """
        result = self.client.write_register(address=address, value=value, device_id=self.device_address)

        if result.isError():
            msg = "Failed to write to single register."
            f"device_address={self.device_address} address={address} count={value}"
            raise ModbusException(msg)

    def _unpack(self, regs: list[int], count: int) -> int:
        """Unpack registers.

        Internal helper to unpuck register list.
        """
        if count and len(regs) == self.INT16_REG_COUNT:
            return regs[0]

        if count and len(regs) == self.INT32_REG_COUNT:
            return (regs[1] << 16) + regs[0]
        msg = f"Failed to unpack register, not speciefied. device_address={self.device_address} regs={regs}"
        raise ModbusException(msg)

    @property
    def v(self) -> float:
        """Voltage (V).

        Returns:
            float: Current voltage value.
        """
        regs = self._read_input_registers(0, self.INT32_REG_COUNT)
        return self._unpack(regs, self.INT32_REG_COUNT) / 10

    @property
    def a(self) -> float:
        """Current (A).

        Returns:
            float: Current ampere value.
        """
        regs = self._read_input_registers(2, self.INT32_REG_COUNT)
        return self._unpack(regs, self.INT32_REG_COUNT) / 1000

    @property
    def password(self) -> int:
        """Password.

        Returns:
            float: Current password value.
        """
        regs = self._read_input_registers(4096, self.INT16_REG_COUNT)
        return self._unpack(regs, self.INT16_REG_COUNT)

    @password.setter
    def password(self, value: int) -> None:
        """Password.

        value: numerical password.
        Min value: 0 (no password)
        Max value: 0000 - 9999.

        Args:
            value (int): Set Password.
        """
        if value not in range(10000):
            msg = f"Invalid password value: {value}. Must be between 0 and 9999."
            raise ValueError(msg)
        self._write_register(4096, value)
