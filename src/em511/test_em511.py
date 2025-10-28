# ruff: noqa: S101,PLR2004, N802

"""Test file for driver."""

from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from em511 import Em511


def test_V() -> None:
    """Test Get v."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.V
    assert value == Decimal("230.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.V
    assert value == Decimal("10500.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.V

    """Test 6: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.V


def test_get_A() -> None:
    """Test Get a."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.A
    assert value == Decimal("10.5")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A
    assert value == Decimal("2300.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.A

    """Test 6: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.A


def test_get_Hz() -> None:
    """Test Get HZ."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC]
    client.read_input_registers.return_value = mock_result
    value = meter.Hz
    assert value == Decimal("230.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28]
    client.read_input_registers.return_value = mock_result
    value = meter.Hz
    assert value == Decimal("3946.4")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.Hz

    """Test 6: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.Hz


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

    """Test 2: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.password

    """Test 3: Should raise exception if password return a value out of its range of 0-9999."""
    mock_result.registers = [0x186A0, 0x0000]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid password value: "):
        _ = meter.password


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

    client.write_register.reset_mock()

    """Test 2: Try set password out of range."""
    with pytest.raises(ValueError, match="Invalid password value:"):
        meter.password = 12345

    """Test 3: Try set password at maximum value."""
    mock_result.registers = [4096]
    client.write_register.return_value = mock_result
    meter.password = 9999
    client.write_register.assert_called_once_with(address=4096, value=9999, device_id=1)

    client.write_register.reset_mock()

    """Test 4: Try set password at lowest value."""
    mock_result.registers = [4096]
    client.write_register.return_value = mock_result
    meter.password = 0
    client.write_register.assert_called_once_with(address=4096, value=0, device_id=1)
