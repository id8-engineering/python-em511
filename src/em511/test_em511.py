# ruff: noqa: S101,PLR2004
"""Test file for driver."""

from unittest.mock import MagicMock

import pytest
from pymodbus.exceptions import ModbusException

from em511 import Em511


def test_v() -> None:
    """Test Get v."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.v
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.v
    assert value == 10500

    """Test 3: Should raise exception due to more registers in use then wanted."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ModbusException):
        _ = meter.v


def test_get_a() -> None:
    """Test Get a."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.a
    assert value == 10.5

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.a
    assert value == 2300

    """Test 3: Should raise exception due to more registers in use then wanted."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ModbusException):
        _ = meter.a


def test_get_password() -> None:
    """Test Get password."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [1234]
    client.read_input_registers.return_value = mock_result
    value = meter.password
    assert value == 1234


def test_set_password() -> None:
    """Test Set Password."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set password"""
    mock_result.registers = [4096]
    client.write_register.return_value = mock_result
    meter.password = 1236
    client.write_register.assert_called_once_with(address=4096, value=1236, device_id=1)

    """Test 2: Try set password out of range."""
    with pytest.raises(ValueError, match="Invalid password value:"):
        meter.password = 12345
