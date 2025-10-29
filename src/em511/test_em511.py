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

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
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

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.A


def test_get_W() -> None:
    """Test Get w."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W
    assert value == Decimal("1050.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.W
    assert value == Decimal("230000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.W

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.W


def test_get_W_dmd() -> None:
    """Test Get w_dmd."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd
    assert value == Decimal("1050.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd
    assert value == Decimal("230000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.W_dmd

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.W_dmd


def test_get_W_dmd_peak() -> None:
    """Test Get w_dmd_peak."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd_peak
    assert value == Decimal("1050.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd_peak
    assert value == Decimal("230000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.W_dmd_peak

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.W_dmd_peak


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

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.Hz


def test_kWh_tot() -> None:
    """Test Get total kWh."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.kWh_tot
    assert value == Decimal("230.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.kWh_tot
    assert value == Decimal("10500.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.kWh_tot

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.kWh_tot


def test_kWh_partial() -> None:
    """Test Get partial kWh."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.kWh_partial
    assert value == Decimal("230.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.kWh_partial
    assert value == Decimal("10500.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.kWh_partial

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.kWh_partial


def test_get_hour_counter() -> None:
    """Test Get hour_counter."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter
    assert value == Decimal("105.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter
    assert value == Decimal("23000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.hour_counter

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.hour_counter


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


def test_get_device_id() -> None:
    """Test Get device id/address."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0xF7]
    client.read_input_registers.return_value = mock_result
    value = meter.device_id
    assert value == 247

    """Test 2: Should pass."""
    mock_result.registers = [0x1]
    client.read_input_registers.return_value = mock_result
    value = meter.device_id
    assert value == 1

    """Test 3: Should raise exception due to value not in range"""
    mock_result.registers = [0x1860]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid device address value: "):
        _ = meter.device_id

    """Test 4: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.device_id

    """Test 5: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.device_id


def test_get_baud_rate() -> None:
    """Test Get baud_rate."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x5]
    client.read_input_registers.return_value = mock_result
    value = meter.baud_rate
    assert value == 5

    """Test 2: Should pass."""
    mock_result.registers = [0x1]
    client.read_input_registers.return_value = mock_result
    value = meter.baud_rate
    assert value == 1

    """Test 3: Should raise exception due to value not in range"""
    mock_result.registers = [0x6]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid baud rate value:"):
        _ = meter.baud_rate

    """Test 4: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.baud_rate

    """Test 5: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.baud_rate


def test_get_parity() -> None:
    """Test Get parity."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2]
    client.read_input_registers.return_value = mock_result
    value = meter.parity
    assert value == 2

    """Test 2: Should pass."""
    mock_result.registers = [0x1]
    client.read_input_registers.return_value = mock_result
    value = meter.parity
    assert value == 1

    """Test 3: Should raise exception due to value not in range"""
    mock_result.registers = [0x3]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid parity value:"):
        _ = meter.parity

    """Test 4: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.parity

    """Test 5: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.parity


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
