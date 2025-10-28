"""Driver class for Carlo Gavazzi EM511 Modbus energy meters.

This module provides a generic, configurable driver for the Carlo Gavazzi EM511
series of energy meters, using pymodbus for serial communication.

The design uses dataclasses to define register specifications and a class
decorator to automatically generate @property accessors for all defined
registers. This minimizes boilerplate and ensures consistency across multiple
registers.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Final, TypeVar

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

T = TypeVar("T", bound=type)


@dataclass(frozen=True)
class RegisterSpec:
    """Specification for a Modbus register mapping.

    Defines the register address, scaling, precision, and read/write behavior.

    Attributes:
        address (int): Modbus register address.
        count (int): Number of consecutive registers to read.
        scale (int): Scaling factor to apply to the raw integer value.
        decimals (int): Number of decimal places to round the scaled value to.
        writable (bool): Whether this register can be written to.
        range (bool): Whether range validation should be performed.
        min (int): Minimum allowed value for range validation.
        max (int): Maximum allowed value for range validation.
    """

    address: int
    count: int
    scale: int
    decimals: int
    writable: bool = False
    range: bool = False
    min: int = 0
    max: int = 0x7FFFFFFF


def register_properties(cls: T) -> T:
    """Class decorator that auto-generates @property accessors for Modbus registers.

    For each entry in `cls._register_specs`, this decorator dynamically creates
    a corresponding @property getter, and optionally a setter if `writable=True`.

    The generated getter automatically calls `_read_register(register_name)`
    and the setter calls `_write_register(address, value)` with range validation
    if enabled in the `RegisterSpec`.

    Args:
        cls: The target class to which properties will be added.

    Returns:
        The same class with dynamically added properties.
    """
    for name, spec in cls._register_specs.items():

        def getter(self: "Em511", _name: str = name, _spec: "RegisterSpec" = spec) -> Decimal:
            """Auto-generated register reader.

            Returns the current value of the register. If range validation is
            enabled, ensures that the returned value is within the expected range.

            Raises:
                ValueError: If the register value is outside its defined range.
            """
            _value = self._read_register(_name)
            if _spec.range and not (_spec.min <= _value <= _spec.max):
                msg = f"Invalid value for '{_name}': {_value}. Must be between {_spec.min} and {_spec.max}."
                raise ValueError(msg)
            return _value

        def setter(self: "Em511", value: int, _name: str = name, _spec: "RegisterSpec" = spec) -> None:
            """Auto-generated register writer.

            Writes a new value to the register and performs range validation
            if defined in the corresponding `RegisterSpec`.

            Raises:
                AttributeError: If the register is read-only.
                ValueError: If the written value is outside its defined range.
            """
            if not _spec.writable:
                msg = f"Register '{_name}' is read-only."
                raise AttributeError(msg)

            if _spec.range and not (_spec.min <= value <= _spec.max):
                msg = f"Invalid value for '{_name}': {value}. Must be between {_spec.min} and {_spec.max}."
                raise ValueError(msg)
            self._write_register(_spec.address, int(value))

        prop = property(getter, setter) if spec.writable else property(getter)

        prop.__doc__ = f"{name} ({'read/write' if spec.writable else 'read-only'})" + (
            f" range=[{spec.min}, {spec.max}]" if spec.range else ""
        )

        setattr(cls, name, prop)

    return cls


@register_properties
class Em511:
    """Driver for Carlo Gavazzi EM511 series energy meters.

    Provides read and write access to Modbus registers via an existing
    `pymodbus.client.ModbusSerialClient` instance. Register definitions are
    dynamically mapped to @property accessors based on `_register_specs`.
    """

    INT16_REG_COUNT = 1
    INT32_REG_COUNT = 2

    INPUT_MAX_VALUE_32 = 0x7FFFFFFF
    INPUT_MAX_VALUE_16 = 0x7FFF

    _register_specs: Final[dict[str, RegisterSpec]] = {
        "V": RegisterSpec(address=0x0000, count=2, scale=10, decimals=1),
        "A": RegisterSpec(address=0x0002, count=2, scale=1000, decimals=3),
        "password": RegisterSpec(
            address=0x1000, count=1, scale=1, decimals=0, writable=True, range=True, min=0, max=9999
        ),
    }

    def __init__(self, device_address: int, client: ModbusSerialClient) -> None:
        """Initialize an Em511 driver instance.

        Args:
            device_address: Modbus address for the EM511 meter.
            client: A connected `ModbusSerialClient` instance.
        """
        self.device_address = device_address
        self.client = client

    def _read_input_registers(self, address: int, count: int) -> list[int]:
        """Safely read input registers from the Modbus device.

        Args:
            address: Starting register address to read.
            count: Number of registers to read.

        Returns:
            A list of integer register values.

        Raises:
            ModbusException: If the read operation fails or returns an error.
        """
        result = self.client.read_input_registers(address=address, count=count, device_id=self.device_address)
        if result.isError():
            msg = (
                "Failed to read input register. "
                f"device_address={self.device_address} address={address} count={count} result={result}"
            )
            raise ModbusException(msg)
        return result.registers

    def _read_register(self, register_name: str) -> Decimal:
        """Read and scale the specified register.

        Args:
            register_name: Name of the register as defined in `_register_specs`.

        Returns:
            A Decimal value representing the scaled register reading.

        Raises:
            ValueError: If register unpacking fails or returns overflow values.
            ModbusException: If Modbus read operation fails.
        """
        spec = self._register_specs[register_name]
        regs = self._read_input_registers(spec.address, spec.count)
        value = Decimal(self._unpack(regs, spec.address)) / spec.scale
        return round(value, spec.decimals)

    def _write_register(self, address: int, value: int) -> None:
        """Write a single Modbus register.

        Args:
            address: Register address to write.
            value: Integer value to write to the register.

        Raises:
            ModbusException: If the write operation fails.
        """
        result = self.client.write_register(address=address, value=value, device_id=self.device_address)
        if result.isError():
            msg = (
                "Failed to write to single register. "
                f"device_address={self.device_address} address={address} value={value}"
            )
            raise ModbusException(msg)

    def _unpack(self, regs: list[int], address: int) -> int:
        """Unpack raw Modbus register data into an integer value.

        Supports both 16-bit and 32-bit register combinations and performs
        overflow detection for "EEE" values reported by the meter.

        Args:
            regs: The list of register values to unpack.
            address: The base register address (used for error reporting).

        Returns:
            The unpacked integer representation of the registers.

        Raises:
            ValueError: If an invalid number of registers is provided or an
                overflow marker is detected.
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

        msg = f"Unexpected register count: {len(regs)} for address={address}"
        raise ValueError(msg)
