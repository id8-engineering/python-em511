# ruff: noqa: N802
"""Driver class for EM511."""

from decimal import Decimal

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException


class Em511:
    """Driver for Carlo Gavazzi EM511 series energy meters.

    This class provides read and write access to Modbus registers
    via a connected `pymodbus.client.ModbusSerialClient` instance.

    Attributes:
        device_address (int): Modbus address of the target device.
        client (ModbusSerialClient): Connected Modbus client.
    """

    INT16_REG_COUNT = 1
    INT32_REG_COUNT = 2

    PASSWORD_MIN_VALUE = 0
    PASSWORD_MAX_VALUE = 9999
    INPUT_MAX_VALUE_32 = 0x7FFFFFFF
    INPUT_MAX_VALUE_16 = 0x7FFF

    EM511_REGISTER_V = 0x0
    EM511_REGISTER_A = 0x2
    EM511_REGISTER_W = 0x4
    EM511_REGISTER_W_DMD = 0xA
    EM511_REGISTER_HZ = 0xF
    EM511_REGISTER_PASSWORD = 0x1000
    EM511_REGISTER_KWH_TOT = 0x10
    EM511_REGISTER_KWH_PARTIAL = 0x14

    SCALE_10 = 10
    SCALE_100 = 100
    SCALE_1000 = 1000

    def __init__(self, device_address: int, client: ModbusSerialClient) -> None:
        """Initialize an Em511 driver instance with an existing Modbus client.

        Args:
            device_address: Modbus address for the EM511 meter.
            client: An initialized ModbusSerialClient instance to use for communication.
        """
        self.device_address = device_address
        self.client = client

    def _read_input_registers(self, address: int, count: int) -> list[int]:
        """Read input registers.

        Internal helper to read Modbus registers safely.

        Args:
            address: Register address to read from.
            count: Number of register to read from.

        Returns:
            list of registers.

        Raises:
            ModbusException: If read operation fails.
        """
        result = self.client.read_input_registers(address=address, count=count, device_id=self.device_address)
        if result.isError():
            msg = (
                "Failed to read input register. "
                f"device_address={self.device_address} address={address} count={count} result={result} "
            )
            raise ModbusException(msg)
        return result.registers

    def _write_register(self, address: int, value: int) -> None:
        """Write to register.

        Internal helper to write to single register.

        Args:
            address: Register to write to.
            value: Value to write the given register with.

        Raises:
            ModbusException: If write operation fails.
        """
        result = self.client.write_register(address=address, value=value, device_id=self.device_address)

        if result.isError():
            msg = (
                "Failed to write to single register."
                f"device_address={self.device_address} address={address} count={value}"
            )
            raise ModbusException(msg)

    def _unpack(self, regs: list[int], address: int) -> int:
        """Unpack registers.

        Internal helper to unpack register list.

        Args:
            regs: List of registers to unpack.
            address: address to the register.

        Returns:
            Unpacked integer value.

        Raises:
            ValueError: If unexpected number of registers is given.
        """
        if len(regs) == self.INT16_REG_COUNT:
            value = regs[0]
            if value == self.INPUT_MAX_VALUE_16:
                msg = f"Input overflow EEE for 16-bit register: device_address={self.device_address} address={address}"
                raise ValueError(msg)
            return value

        if len(regs) == self.INT32_REG_COUNT:
            value = (regs[1] << 16) + regs[0]
            if value == self.INPUT_MAX_VALUE_32:
                msg = f"Input overflow EEE for 32-bit register: device_address={self.device_address} address={address}"
                raise ValueError(msg)
            return value

        msg = f"Unexpected register count: {len(regs)}."
        raise ValueError(msg)

    @property
    def V(self) -> Decimal:
        """Voltage (V).

        Returns:
            Decimal: Current voltage value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_V, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_V)) / self.SCALE_10
        return round(value, 1)

    @property
    def A(self) -> Decimal:
        """Current (A).

        Returns:
            Decimal: Current ampere value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_A, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_A)) / self.SCALE_1000
        return round(value, 3)

    @property
    def W(self) -> Decimal:
        """Power (W).

        Returns:
            Decimal: Current watt value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_W, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_W)) / self.SCALE_10
        return round(value, 1)

    @property
    def W_dmd(self) -> Decimal:
        """Power (W_dmd).

        Returns:
            Decimal: Current watt demand value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_W_DMD, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_W_DMD)) / self.SCALE_10
        return round(value, 1)

    @property
    def Hz(self) -> Decimal:
        """Hertz (Hz).

        Returns:
            Decimal: Current hertz value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_HZ, self.INT16_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_HZ)) / self.SCALE_10
        return round(value, 1)

    @property
    def kWh_tot(self) -> Decimal:
        """Kilo watt hours in total (kWh).

        Returns:
            Decimal: Current total kWh value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_KWH_TOT, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_KWH_TOT)) / self.SCALE_10
        return round(value, 1)

    @property
    def kWh_partial(self) -> Decimal:
        """Kilo watt hours partial (kWh).

        Returns:
            Decimal: Current partial kWh value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_KWH_PARTIAL, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_KWH_PARTIAL)) / self.SCALE_10
        return round(value, 1)

    @property
    def password(self) -> int:
        """Password.

        Returns:
            int: Current password value.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If password is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_PASSWORD, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_PASSWORD)
        if not (self.PASSWORD_MIN_VALUE <= value <= self.PASSWORD_MAX_VALUE):
            msg = f"Invalid password value: {value}. Must be between 0 and 9999."
            raise ValueError(msg)
        return value

    @password.setter
    def password(self, value: int) -> None:
        """Password.

        Min value: 0 (no password).
        Max value: 9999.

        Args:
            value (int): Set Password.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If password value is out of range.
        """
        if not (self.PASSWORD_MIN_VALUE <= value <= self.PASSWORD_MAX_VALUE):
            msg = f"Invalid password value: {value}. Must be between 0 and 9999."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_PASSWORD, value)
