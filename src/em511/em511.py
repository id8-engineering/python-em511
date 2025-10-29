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
    DEVICE_ADDRESS_MAX_VALUE = 247
    DEVICE_ADDRESS_MIN_VALUE = 1
    BAUD_RATE_MIN_VALUE = 1
    BAUD_RATE_MAX_VALUE = 5
    PARITY_MIN_VALUE = 1
    PARITY_MAX_VALUE = 2
    STOP_BIT_MIN_VALUE = 0
    STOP_BIT_MAX_VALUE = 1
    REPLY_DELAY_MIN_VALUE = 0
    REPLY_DELAY_MAX_VALUE = 1000

    EM511_REGISTER_V = 0x0
    EM511_REGISTER_A = 0x2
    EM511_REGISTER_A_DMD = 0x3A
    EM511_REGISTER_A_DMD_PEAK = 0x3C
    EM511_REGISTER_W = 0x4
    EM511_REGISTER_W_DMD = 0xA
    EM511_REGISTER_W_DMD_PEAK = 0xC
    EM511_REGISTER_HZ = 0xF
    EM511_REGISTER_PASSWORD = 0x1000
    EM511_REGISTER_KWH_TOT = 0x10
    EM511_REGISTER_KWH_PARTIAL = 0x14
    EM511_REGISTER_HOUR_COUNTER = 0x2C
    EM511_REGISTER_LIFETIME_COUNTER = 0x30
    EM511_REGISTER_HOUR_COUNTER_PART = 0x36
    EM511_REGISTER_DEVICE_ID = 0x2000
    EM511_REGISTER_BAUD_RATE = 0x2001
    EM511_REGISTER_PARITY = 0x2002
    EM511_REGISTER_STOP_BIT = 0x2003
    EM511_REGISTER_REPLY_DELAY = 0x2004
    EM511_REGISTER_RESET_TOT_ENERGY_AND_RUN_HOUR_COUNTER = 0x4003
    EM511_REGISTER_RESET_PARTIAL_ENERGY_AND_HOUR_COUNTER = 0x4004
    EM511_REGISTER_RESET_TO_FACTORY_SETTINGS = 0x4020

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
                "Failed to write to single register: "
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
    def A_dmd(self) -> Decimal:
        """Current demand (A).

        Returns:
            Decimal: Current demand ampere value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_A_DMD, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_A_DMD)) / self.SCALE_1000
        return round(value, 3)

    @property
    def A_dmd_peak(self) -> Decimal:
        """Current demand peak (A).

        Returns:
            Decimal: Current demand peak, ampere value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_A_DMD_PEAK, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_A_DMD_PEAK)) / self.SCALE_1000
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
    def W_dmd_peak(self) -> Decimal:
        """Power (W_dmd_peak).

        Returns:
            Decimal: Current watt demand peak value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_W_DMD_PEAK, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_W_DMD_PEAK)) / self.SCALE_10
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
    def hour_counter(self) -> Decimal:
        """Run time in hours (h).

        Returns:
            Decimal: Run time in hours value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_HOUR_COUNTER, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_HOUR_COUNTER)) / self.SCALE_100
        return round(value, 2)

    @property
    def lifetime_counter(self) -> Decimal:
        """Lifetime in hours (h).

        Returns:
            Decimal: Lifetime in hours value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_LIFETIME_COUNTER, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_LIFETIME_COUNTER)) / self.SCALE_100
        return round(value, 2)

    @property
    def hour_counter_part(self) -> Decimal:
        """Partial run-hour counter (h).

        Returns:
            Decimal: partial operating tim in hours value.

        Raises:
            ValueError: If input is at max value or above.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_HOUR_COUNTER_PART, self.INT32_REG_COUNT)
        value = Decimal(self._unpack(regs, self.EM511_REGISTER_HOUR_COUNTER_PART)) / self.SCALE_100
        return round(value, 2)

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

    @property
    def device_id(self) -> int:
        """Device address.

        (Default value=1)

        Returns:
            Int: Current device address.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If device address is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_DEVICE_ID, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_DEVICE_ID)
        if not (self.DEVICE_ADDRESS_MIN_VALUE <= value <= self.DEVICE_ADDRESS_MAX_VALUE):
            msg = f"Invalid device address value: {value}. Must be between 1 and 247."
            raise ValueError(msg)
        return value

    @property
    def baud_rate(self) -> int:
        """Baud rate.

        1=9.6kbps, 2=19.2kbps, 3=38.4kbps,
        4=57.6kbps, 5=115.2kbps (default=1)

        Returns:
            Int: Current baud rate.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If baud rate is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_BAUD_RATE, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_BAUD_RATE)
        if not (self.BAUD_RATE_MIN_VALUE <= value <= self.BAUD_RATE_MAX_VALUE):
            msg = f"Invalid baud rate value: {value}. Must be between 1 and 5."
            raise ValueError(msg)
        return value

    @property
    def parity(self) -> int:
        """Parity.

        1=None, 2=Even (default=1)

        Returns:
            Int: Current parity.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If parity is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_PARITY, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_PARITY)
        if not (self.PARITY_MIN_VALUE <= value <= self.PARITY_MAX_VALUE):
            msg = f"Invalid parity value: {value}. Must be between 1 and 2."
            raise ValueError(msg)
        return value

    @property
    def stop_bit(self) -> int:
        """Stop bits.

        0=1 stop bit (default), 1=2 stop bits; fixed to 1 if parity=Even

        Returns:
            Int: Current stop bit value.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If stop bit is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_STOP_BIT, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_STOP_BIT)
        if not (self.STOP_BIT_MIN_VALUE <= value <= self.STOP_BIT_MAX_VALUE):
            msg = f"Invalid stop bit value: {value}. Must be between 1 and 2."
            raise ValueError(msg)
        return value

    @property
    def reply_delay(self) -> int:
        """Reply delay.

        Range: 0-1000 ms (default=0)

        Returns:
            int: Current reply delay value.

        Raises:
            ValueError: If input is at max value or above.
            ValueError: If reply delay is out of range.
            ModbusException: If failed to read input register.
        """
        regs = self._read_input_registers(self.EM511_REGISTER_REPLY_DELAY, self.INT16_REG_COUNT)
        value = self._unpack(regs, self.EM511_REGISTER_REPLY_DELAY)
        if not (self.REPLY_DELAY_MIN_VALUE <= value <= self.REPLY_DELAY_MAX_VALUE):
            msg = f"Invalid reply delay value: {value}. Must be between 0 and 1000."
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

    @device_id.setter
    def device_id(self, value: int) -> None:
        """Device id.

        Range 1 - 247

        Args:
            value (int): Set device id.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If device id value is out of range.
        """
        if not (self.DEVICE_ADDRESS_MIN_VALUE <= value <= self.DEVICE_ADDRESS_MAX_VALUE):
            msg = f"Invalid device id value: {value}. Must be between 1 and 247."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_DEVICE_ID, value)

    @baud_rate.setter
    def baud_rate(self, value: int) -> None:
        """Baud rate.

        1=9.6kbps, 2=19.2kbps, 3=38.4kbps,
        4=57.6kbps, 5=115.2kbps (default=1).

        Args:
            value (int): Set baud rate.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If baud rate value is out of range.
        """
        if not (self.BAUD_RATE_MIN_VALUE <= value <= self.BAUD_RATE_MAX_VALUE):
            msg = f"Invalid baud rate value: {value}. Must be between 1 and 5."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_BAUD_RATE, value)

    @parity.setter
    def parity(self, value: int) -> None:
        """Parity.

        1=None, 2=Even (default=1).


        Args:
            value (int): Set parity.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If parity value is out of range.
        """
        if not (self.PARITY_MIN_VALUE <= value <= self.PARITY_MAX_VALUE):
            msg = f"Invalid parity value: {value}. Must be between 1 and 2."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_PARITY, value)

    @stop_bit.setter
    def stop_bit(self, value: int) -> None:
        """Stop bit.

        0=1 stop bit (default), 1=2 stop bits; fixed to 1 if parity=Even.

        Args:
            value (int): Set stop bit.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If stop bit value is out of range.
        """
        if not (self.STOP_BIT_MIN_VALUE <= value <= self.STOP_BIT_MAX_VALUE):
            msg = f"Invalid stop bit value: {value}. Must be between 0 and 1."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_STOP_BIT, value)

    @reply_delay.setter
    def reply_delay(self, value: int) -> None:
        """Reply delay.

        Range: 0 - 1000 ms (default=0).

        Args:
            value (int): Set reply delay.

        Raises:
            ModbusException: If failed to write to single register.
            ValueError: If reply delay value is out of range.
        """
        if not (self.REPLY_DELAY_MIN_VALUE <= value <= self.REPLY_DELAY_MAX_VALUE):
            msg = f"Invalid reply delay value: {value}. Must be between 0 and 1000."
            raise ValueError(msg)
        self._write_register(self.EM511_REGISTER_REPLY_DELAY, value)

    def reset_tot_energy_and_run_hour_counter(self) -> None:
        """Reset total energy + total run hour counters (excluding lifetime).

        Writes 1 to execute.

        Raises:
            ModbusException: If failed to write to single register.
        """
        self._write_register(self.EM511_REGISTER_RESET_TOT_ENERGY_AND_RUN_HOUR_COUNTER, 1)

    def reset_partial_energy_and_hour_counter(self) -> None:
        """Reset partial energy + partial run hour counters.

        Writes 1 to execute.

        Raises:
            ModbusException: If failed to write to single register.
        """
        self._write_register(self.EM511_REGISTER_RESET_PARTIAL_ENERGY_AND_HOUR_COUNTER, 1)

    def reset_to_factory_settings(self) -> None:
        """Factory Restore (Default settings).

        Write 0x0A0A=2570, then within 1s write 0xC1A0=49568 to trigger reset.

        Raises:
            ModbusException: If failed to write to single register.
        """
        self._write_register(self.EM511_REGISTER_RESET_TO_FACTORY_SETTINGS, 0x0A0A)
        self._write_register(self.EM511_REGISTER_RESET_TO_FACTORY_SETTINGS, 0xC1A0)
