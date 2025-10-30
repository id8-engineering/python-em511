# ruff: noqa: S101,PLR2004, N802

"""Test file for driver."""

from unittest.mock import MagicMock

import pytest

from em511 import Em511


def test_unpack() -> None:
    """Test unpack."""
    client = MagicMock()
    meter = Em511(1, client)

    """Test 1: Should raise exception due to more registers in use than allowed."""
    registers = [0x1860, 0x0023, 0x4244]
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter._unpack(registers, 0x0001)  # noqa: SLF001

    """Test 2: Should raise exception due to 16-bit register overflow"""
    registers = [0x7FFF]
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter._unpack(registers, 0x0001)  # noqa: SLF001

    """Test 3: Should raise exception due to 32-bit register overflow"""
    registers = [0xFFFF, 0x7FFF]
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter._unpack(registers, 0x0001)  # noqa: SLF001


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
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.V
    assert value == 10500


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
    assert value == 10.5

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A
    assert value == 2300


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

    """Test 2: Should raise exception if password return a value out of its range of 0-9999."""
    mock_result.registers = [0x186A0, 0x0000]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
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
    with pytest.raises(ValueError, match="Invalid value for"):
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
