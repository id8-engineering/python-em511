# ruff: noqa: S101,PLR2004, N802

"""Test file for driver."""

from decimal import Decimal
from unittest.mock import MagicMock, call

import pytest
from pymodbus import ModbusException

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


def test_get_A_dmd() -> None:
    """Test Get a_dmd."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd
    assert value == Decimal("10.5")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd
    assert value == Decimal("2300.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.A_dmd

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.A_dmd


def test_get_A_dmd_peak() -> None:
    """Test Get a_dmd_peak."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd_peak
    assert value == Decimal("10.5")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd_peak
    assert value == Decimal("2300.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.A_dmd_peak

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.A_dmd_peak


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


def test_get_lifetime_counter() -> None:
    """Test Get lifetime_counter."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.lifetime_counter
    assert value == Decimal("105.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.lifetime_counter
    assert value == Decimal("23000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.lifetime_counter

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.lifetime_counter


def test_get_life_time_counter() -> None:
    """Test Get hour_counter_partial."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter_part
    assert value == Decimal("105.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter_part
    assert value == Decimal("23000.0")

    """Test 3: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x4244]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.hour_counter_part

    """Test 4: Should raise exception if input value exceeds maximum value, display shows 'EEE', 32-bit register."""
    mock_result.registers = [0xFFFF, 0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter.hour_counter_part


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


def test_get_stop_bit() -> None:
    """Test Get stop_bit."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x1]
    client.read_input_registers.return_value = mock_result
    value = meter.stop_bit
    assert value == 1

    """Test 2: Should pass."""
    mock_result.registers = [0x0]
    client.read_input_registers.return_value = mock_result
    value = meter.stop_bit
    assert value == 0

    """Test 3: Should raise exception due to value not in range"""
    mock_result.registers = [0x2]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid stop bit value:"):
        _ = meter.stop_bit

    """Test 4: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.stop_bit

    """Test 5: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.stop_bit


def test_get_reply_delay() -> None:
    """Test Get reply delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x3E8]
    client.read_input_registers.return_value = mock_result
    value = meter.reply_delay
    assert value == 1000

    """Test 2: Should pass."""
    mock_result.registers = [0x0]
    client.read_input_registers.return_value = mock_result
    value = meter.reply_delay
    assert value == 0

    """Test 3: Should raise exception due to value not in range"""
    mock_result.registers = [0x3E9]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid reply delay value:"):
        _ = meter.reply_delay

    """Test 4: Should raise exception due to more registers in use than allowed."""
    mock_result.registers = [0x1860, 0x0023, 0x5743]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter.reply_delay

    """Test 5: Should raise exception if input value exceeds maximum value, display shows 'EEE', 16-bit register."""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter.reply_delay


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

    """Test 5: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.password = 1


def test_set_device_id() -> None:
    """Test Set device id."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set device id"""
    mock_result.registers = [8192]
    client.write_register.return_value = mock_result
    meter.device_id = 123
    client.write_register.assert_called_once_with(address=8192, value=123, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set device id out of range."""
    with pytest.raises(ValueError, match="Invalid device id value:"):
        meter.device_id = 248

    """Test 3: Try set device id out of range."""
    with pytest.raises(ValueError, match="Invalid device id value:"):
        meter.device_id = 0

    """Test 4: Try set device id at maximum value."""
    mock_result.registers = [8192]
    client.write_register.return_value = mock_result
    meter.device_id = 247
    client.write_register.assert_called_once_with(address=8192, value=247, device_id=1)

    client.write_register.reset_mock()

    """Test 5: Try set device id at lowest value."""
    mock_result.registers = [8192]
    client.write_register.return_value = mock_result
    meter.device_id = 1
    client.write_register.assert_called_once_with(address=8192, value=1, device_id=1)

    """Test 6: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.device_id = 1


def test_set_baud_rate() -> None:
    """Test Set baud rate."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set baud rate"""
    mock_result.registers = [8193]
    client.write_register.return_value = mock_result
    meter.baud_rate = 2
    client.write_register.assert_called_once_with(address=8193, value=2, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set baud rate out of range."""
    with pytest.raises(ValueError, match="Invalid baud rate value:"):
        meter.baud_rate = 6

    """Test 3: Try set baud rate out of range."""
    with pytest.raises(ValueError, match="Invalid baud rate value:"):
        meter.baud_rate = 0

    """Test 4: Try set baud rate at maximum value."""
    mock_result.registers = [8193]
    client.write_register.return_value = mock_result
    meter.baud_rate = 5
    client.write_register.assert_called_once_with(address=8193, value=5, device_id=1)

    client.write_register.reset_mock()

    """Test 5: Try set baud rate at lowest value."""
    mock_result.registers = [8193]
    client.write_register.return_value = mock_result
    meter.baud_rate = 1
    client.write_register.assert_called_once_with(address=8193, value=1, device_id=1)

    """Test 6: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.baud_rate = 1


def test_set_parity() -> None:
    """Test Set parity."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set parity"""
    mock_result.registers = [8194]
    client.write_register.return_value = mock_result
    meter.parity = 1
    client.write_register.assert_called_once_with(address=8194, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set parity out of range."""
    with pytest.raises(ValueError, match="Invalid parity value:"):
        meter.parity = 3

    """Test 3: Try set parity out of range."""
    with pytest.raises(ValueError, match="Invalid parity value:"):
        meter.parity = 0

    """Test 4: Try set parity at maximum value."""
    mock_result.registers = [8194]
    client.write_register.return_value = mock_result
    meter.parity = 2
    client.write_register.assert_called_once_with(address=8194, value=2, device_id=1)

    client.write_register.reset_mock()

    """Test 5: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.parity = 1


def test_set_stop_bit() -> None:
    """Test Set stop bit."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set stop bit"""
    mock_result.registers = [8195]
    client.write_register.return_value = mock_result
    meter.stop_bit = 0
    client.write_register.assert_called_once_with(address=8195, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set stop bit out of range."""
    with pytest.raises(ValueError, match="Invalid stop bit value:"):
        meter.stop_bit = 2

    """Test 3: Try set stop bit at maximum value."""
    mock_result.registers = [8195]
    client.write_register.return_value = mock_result
    meter.stop_bit = 1
    client.write_register.assert_called_once_with(address=8195, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 4: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.stop_bit = 1


def test_set_reply_delay() -> None:
    """Test Set reply delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set reply delay"""
    mock_result.registers = [8196]
    client.write_register.return_value = mock_result
    meter.reply_delay = 0
    client.write_register.assert_called_once_with(address=8196, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set reply delay out of range."""
    with pytest.raises(ValueError, match="Invalid reply delay value:"):
        meter.reply_delay = 1001

    """Test 3: Try set reply delay at maximum value."""
    mock_result.registers = [8196]
    client.write_register.return_value = mock_result
    meter.reply_delay = 1000
    client.write_register.assert_called_once_with(address=8196, value=1000, device_id=1)

    """Test 4: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.reply_delay = 1


def test_reset_tot_energy_and_run_hour_counter() -> None:
    """Test Reset total energy and run hour counter."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Reset"""
    mock_result.registers = [16387]
    client.write_register.return_value = mock_result
    meter.reset_tot_energy_and_run_hour_counter()
    client.write_register.assert_called_once_with(address=16387, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 4: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.reset_tot_energy_and_run_hour_counter()


def test_reset_partial_energy_and_hour_counter() -> None:
    """Test Reset partial energy + partial hour counters."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Reset"""
    mock_result.registers = [16388]
    client.write_register.return_value = mock_result
    meter.reset_partial_energy_and_hour_counter()
    client.write_register.assert_called_once_with(address=16388, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 4: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.reset_partial_energy_and_hour_counter()


def test_reset_to_factory_settings() -> None:
    """Test Reset DMD and DMD max values."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    client.write_register.return_value = mock_result
    meter = Em511(1, client)

    """Test 1: Both writes occur"""
    meter.reset_to_factory_settings()
    expected_calls = [
        call(address=16416, value=0x0A0A, device_id=1),
        call(address=16416, value=0xC1A0, device_id=1),
    ]
    assert client.write_register.call_args_list == expected_calls
    assert client.write_register.call_count == 2

    """Test 3: Should raise exception due to failed writing to single register."""
    mock_result.isError.return_value = True
    client.write_register.return_value = mock_result
    with pytest.raises(ModbusException, match="Failed to write to single register:"):
        meter.reset_to_factory_settings()
