# ruff: noqa: S101, PLR2004, N802, SLF001
"""Test file for driver."""

from decimal import Decimal
from unittest.mock import MagicMock, call

import pytest

from em511 import Em511


def test_unpack() -> None:
    """Test unpack."""
    client = MagicMock()
    meter = Em511(1, client)

    """Test 1: Should raise exception due to more registers in use than allowed."""
    registers = [0x1860, 0x0023, 0x4244]
    with pytest.raises(ValueError, match="Unexpected register count:"):
        _ = meter._unpack(registers, 0x0001)

    """Test 2: Should raise exception due to 16-bit register overflow"""
    registers = [0x7FFF]
    with pytest.raises(ValueError, match="Input overflow EEE for 16-bit register: "):
        _ = meter._unpack(registers, 0x0001)

    """Test 3: Should raise exception due to 32-bit register overflow"""
    registers = [0xFFFF, 0x7FFF]
    with pytest.raises(ValueError, match="Input overflow EEE for 32-bit register: "):
        _ = meter._unpack(registers, 0x0001)


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


def test_get_A_dmd() -> None:
    """Test get A dmd."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass."""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd
    assert value == 10.5

    """Test 1: should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd
    assert value == 2300


def test_get_A_dmd_peak() -> None:
    """Test get A dmd peak."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass."""
    mock_result.registers = [0x2904, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd_peak
    assert value == 10.5

    """Test 1: should pass."""
    mock_result.registers = [0x1860, 0x0023]
    client.read_input_registers.return_value = mock_result
    value = meter.A_dmd_peak
    assert value == 2300


def test_W() -> None:
    """Test Get W."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.W
    assert value == 10500


def test_W_dmd() -> None:
    """Test Get W dmd."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd
    assert value == 10500


def test_W_dmd_peak() -> None:
    """Test Get W dmd peak."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd_peak
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.W_dmd_peak
    assert value == 10500


def test_get_Hz() -> None:
    """Test Get Hz."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [1234]
    client.read_input_registers.return_value = mock_result
    value = meter.Hz
    assert value == Decimal("123.4")

    """Test 2: Should raise exception due to 16-bit register overflow"""
    mock_result.registers = [0x7FFF]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Input overflow EEE"):
        _ = meter.Hz


def test_get_kwh_tot() -> None:
    """Test Get kwh tot."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.kwh_tot
    assert value == 230

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.kwh_tot
    assert value == 10500


def test_get_kwh_partial() -> None:
    """Test Get kwh partial."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: should pass"""
    mock_result.registers = [0x08FC, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.kwh_partial
    assert value == Decimal("230.0")

    """Test 2: Should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.kwh_partial
    assert value == Decimal("10500.0")


def test_get_hour_counter() -> None:
    """Test Get hour counter."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Should pass."""
    mock_result.registers = [0x142D, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter
    assert value == Decimal("51.65")

    """Test 2: should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter
    assert value == Decimal("1050.00")


def test_get_lifetime_counter() -> None:
    """Test Get lifetime counter."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Should pass."""
    mock_result.registers = [0x142D, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.lifetime_counter
    assert value == Decimal("51.65")

    """Test 2: should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.lifetime_counter
    assert value == Decimal("1050.00")


def test_get_hour_counter_part() -> None:
    """Test Get hour counter partial."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Should pass."""
    mock_result.registers = [0x142D, 0x0000]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter_part
    assert value == Decimal("51.65")

    """Test 2: should pass."""
    mock_result.registers = [0x9A28, 0x0001]
    client.read_input_registers.return_value = mock_result
    value = meter.hour_counter_part
    assert value == Decimal("1050.00")


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


def test_get_alarm_status() -> None:
    """Test Get alarm status."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_status
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_status
    assert value == 1

    """Test 3: Should raise exception if returned value is out of range 0 - 1."""
    mock_result.registers = [2]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.alarm_status


def test_get_alarm_mode() -> None:
    """Test Get alarm mode."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_mode
    assert value == 1

    """"Test 2: Should pass."""
    mock_result.registers = [6]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_mode
    assert value == 6

    """Test 3: Should raise exception if returned value is out of range 1 - 6."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.alarm_mode


def test_get_alarm_delay() -> None:
    """Test Get alarm delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_delay
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [3600]
    client.read_input_registers.return_value = mock_result
    value = meter.alarm_delay
    assert value == 3600

    """Test 3: Should raise exception if returned value is out of range 0 - 3600."""
    mock_result.registers = [3601]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.alarm_delay


def test_get_dmd_integration_time() -> None:
    """Test Get dmd integration time."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.dmd_integration_time
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [6]
    client.read_input_registers.return_value = mock_result
    value = meter.dmd_integration_time
    assert value == 6

    """Test 3: Should raise exception if returned value is out of range 0 - 6."""
    mock_result.registers = [7]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.dmd_integration_time


def test_get_device_id() -> None:
    """Test Get device id."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.device_id
    assert value == 1

    """"Test 2: Should pass."""
    mock_result.registers = [247]
    client.read_input_registers.return_value = mock_result
    value = meter.device_id
    assert value == 247

    """Test 3: Should raise exception if returned value is out of range 1 - 247."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.device_id


def test_get_baud_rate() -> None:
    """Test Get baud rate."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.baud_rate
    assert value == 1

    """"Test 2: Should pass."""
    mock_result.registers = [5]
    client.read_input_registers.return_value = mock_result
    value = meter.baud_rate
    assert value == 5

    """Test 3: Should raise exception if returned value is out of range 1 - 5."""
    mock_result.registers = [6]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.baud_rate


def test_get_parity() -> None:
    """Test Get parity."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.parity
    assert value == 1

    """"Test 2: Should pass."""
    mock_result.registers = [2]
    client.read_input_registers.return_value = mock_result
    value = meter.parity
    assert value == 2

    """Test 3: Should raise exception if returned value is out of range 1 - 2."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.parity


def test_get_stop_bit() -> None:
    """Test Get stop bit."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.stop_bit
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.stop_bit
    assert value == 1

    """Test 3: Should raise exception if returned value is out of range 0 - 1."""
    mock_result.registers = [2]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.stop_bit


def test_get_reply_delay() -> None:
    """Test Get reply delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.reply_delay
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [1000]
    client.read_input_registers.return_value = mock_result
    value = meter.reply_delay
    assert value == 1000

    """Test 3: Should raise exception if returned value is out of range 0 - 1."""
    mock_result.registers = [1001]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.reply_delay


def test_get_identification_code() -> None:
    """Test Get stop bit."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [1792]
    client.read_input_registers.return_value = mock_result
    value = meter.identification_code
    assert value == 1792

    """"Test 2: Should pass."""
    mock_result.registers = [1795]
    client.read_input_registers.return_value = mock_result
    value = meter.identification_code
    assert value == 1795

    """Test 3: Should raise exception if returned value is out of range 0 - 1."""
    mock_result.registers = [1001]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.identification_code


def test_get_measure_mode() -> None:
    """Test Get stop bit."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: Should pass."""
    mock_result.registers = [0]
    client.read_input_registers.return_value = mock_result
    value = meter.measure_mode
    assert value == 0

    """"Test 2: Should pass."""
    mock_result.registers = [1]
    client.read_input_registers.return_value = mock_result
    value = meter.measure_mode
    assert value == 1

    """Test 3: Should raise exception if returned value is out of range 0 - 1."""
    mock_result.registers = [1001]
    client.read_input_registers.return_value = mock_result
    with pytest.raises(ValueError, match="Invalid value for"):
        _ = meter.measure_mode


def test_set_password() -> None:
    """Test Set Password."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set password"""
    mock_result.registers = [0x1000]
    client.write_register.return_value = mock_result
    meter.password = 1236
    client.write_register.assert_called_once_with(address=0x1000, value=1236, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set password out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.password = 12345

    """Test 3: Try set password at maximum value."""
    mock_result.registers = [0x1000]
    client.write_register.return_value = mock_result
    meter.password = 9999
    client.write_register.assert_called_once_with(address=0x1000, value=9999, device_id=1)

    client.write_register.reset_mock()

    """Test 4: Try set password at lowest value."""
    mock_result.registers = [0x1000]
    client.write_register.return_value = mock_result
    meter.password = 0
    client.write_register.assert_called_once_with(address=0x1000, value=0, device_id=1)


def test_set_alarm_mode() -> None:
    """Test Set alarm mode."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set alarm mode"""
    mock_result.registers = [1]
    client.write_register.return_value = mock_result
    meter.alarm_mode = 1
    client.write_register.assert_called_once_with(address=0x1015, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set alarm mode out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.alarm_mode = 7

    """Test 3: Try set alarm mode at maximum value."""
    mock_result.registers = [6]
    client.write_register.return_value = mock_result
    meter.alarm_mode = 6
    client.write_register.assert_called_once_with(address=0x1015, value=6, device_id=1)

    client.write_register.reset_mock()


def test_set_alarm_delay() -> None:
    """Test Set alarm delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set alarm delay"""
    mock_result.registers = [0]
    client.write_register.return_value = mock_result
    meter.alarm_delay = 0
    client.write_register.assert_called_once_with(address=0x101A, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set alarm delay out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.alarm_delay = 3601

    """Test 3: Try set alarm delay at maximum value."""
    mock_result.registers = [3600]
    client.write_register.return_value = mock_result
    meter.alarm_delay = 3600
    client.write_register.assert_called_once_with(address=0x101A, value=3600, device_id=1)

    client.write_register.reset_mock()


def test_set_dmd_integration_time() -> None:
    """Test Set dmd integration time."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set dmd integration time"""
    mock_result.registers = [0]
    client.write_register.return_value = mock_result
    meter.dmd_integration_time = 0
    client.write_register.assert_called_once_with(address=0x1010, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set dmd integration time out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.dmd_integration_time = 7

    """Test 3: Try set dmd integration time at maximum value."""
    mock_result.registers = [6]
    client.write_register.return_value = mock_result
    meter.dmd_integration_time = 6
    client.write_register.assert_called_once_with(address=0x1010, value=6, device_id=1)

    client.write_register.reset_mock()


def test_set_device_id() -> None:
    """Test Set device id."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set device id"""
    mock_result.registers = [1]
    client.write_register.return_value = mock_result
    meter.device_id = 1
    client.write_register.assert_called_once_with(address=0x2000, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set device id out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.device_id = 248

    """Test 3: Try set device id at maximum value."""
    mock_result.registers = [247]
    client.write_register.return_value = mock_result
    meter.device_id = 247
    client.write_register.assert_called_once_with(address=0x2000, value=247, device_id=1)

    client.write_register.reset_mock()


def test_set_baud_rate() -> None:
    """Test Set baud rate."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set baud rate"""
    mock_result.registers = [1]
    client.write_register.return_value = mock_result
    meter.baud_rate = 1
    client.write_register.assert_called_once_with(address=0x2001, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set baud rate out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.baud_rate = 6

    """Test 3: Try set baud rate at maximum value."""
    mock_result.registers = [5]
    client.write_register.return_value = mock_result
    meter.baud_rate = 5
    client.write_register.assert_called_once_with(address=0x2001, value=5, device_id=1)

    client.write_register.reset_mock()


def test_set_parity() -> None:
    """Test Set parity."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set parity"""
    mock_result.registers = [1]
    client.write_register.return_value = mock_result
    meter.parity = 1
    client.write_register.assert_called_once_with(address=0x2002, value=1, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set parity out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.parity = 3

    """Test 3: Try set parity at maximum value."""
    mock_result.registers = [2]
    client.write_register.return_value = mock_result
    meter.parity = 2
    client.write_register.assert_called_once_with(address=0x2002, value=2, device_id=1)

    client.write_register.reset_mock()


def test_set_stop_bit() -> None:
    """Test Set alarm delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set alarm delay"""
    mock_result.registers = [0]
    client.write_register.return_value = mock_result
    meter.stop_bit = 0
    client.write_register.assert_called_once_with(address=0x2003, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set alarm delay out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.stop_bit = 2

    """Test 3: Try set alarm delay at maximum value."""
    mock_result.registers = [1]
    client.write_register.return_value = mock_result
    meter.stop_bit = 1
    client.write_register.assert_called_once_with(address=0x2003, value=1, device_id=1)

    client.write_register.reset_mock()


def test_set_reply_delay() -> None:
    """Test Set reply delay."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """Test 1: Set reply delay"""
    mock_result.registers = [0]
    client.write_register.return_value = mock_result
    meter.reply_delay = 0
    client.write_register.assert_called_once_with(address=0x2004, value=0, device_id=1)

    client.write_register.reset_mock()

    """Test 2: Try set reply delay out of range."""
    with pytest.raises(ValueError, match="Invalid value for"):
        meter.reply_delay = 1001

    """Test 3: Try set reply delay at maximum value."""
    mock_result.registers = [1000]
    client.write_register.return_value = mock_result
    meter.reply_delay = 1000
    client.write_register.assert_called_once_with(address=0x2004, value=1000, device_id=1)

    client.write_register.reset_mock()


def test_reset_tot_energy_and_run_hour_counter() -> None:
    """Test to reset tot_energy_and_run_hour_counter."""
    client = MagicMock()
    meter = Em511(1, client)
    meter._write_register = MagicMock()

    meter.reset_tot_energy_and_run_hour_counter()

    meter._write_register.assert_called_once_with(meter.EM511_REGISTER_RESET_TOT_ENERGY_AND_RUN_HOUR_COUNTER, 1)


def test_reset_partial_energy_and_hour_counter() -> None:
    """Test to reset partial energy and hour counter."""
    client = MagicMock()
    meter = Em511(1, client)
    meter._write_register = MagicMock()

    meter.reset_partial_energy_and_hour_counter()

    meter._write_register.assert_called_once_with(meter.EM511_REGISTER_RESET_PARTIAL_ENERGY_AND_HOUR_COUNTER, 1)


def test_reset_dmd_and_dmd_max() -> None:
    """Test to reset DMD and DMD max values."""
    client = MagicMock()
    meter = Em511(1, client)
    meter._write_register = MagicMock()

    meter.reset_dmd_and_dmd_max()

    meter._write_register.assert_called_once_with(meter.EM511_REGISTER_RESET_DMD_AND_DMD_MAX, 1)


def test_reset_to_factory_settings() -> None:
    """Test to reset to factory default settings."""
    client = MagicMock()
    meter = Em511(1, client)
    meter._write_register = MagicMock()

    meter.reset_to_factory_settings()

    """Factory reset should call _write_register twice with specific values."""
    expected_calls = [
        call(meter.EM511_REGISTER_RESET_TO_FACTORY_SETTINGS, 0x0A0A),
        call(meter.EM511_REGISTER_RESET_TO_FACTORY_SETTINGS, 0xC1A0),
    ]

    """Verify that `reset_to_factory_settings` calls `_write_register` twice with the correct values in order."""
    meter._write_register.assert_has_calls(expected_calls)
    meter._write_register.assert_called()
    assert meter._write_register.call_count == 2


def test_get_firmware_and_revision_code() -> None:
    """Test Get firmware and revision."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    """"Test 1: verify firmware decoding"""
    mock_result.registers = [0x4343]
    client.read_input_registers.return_value = mock_result
    value = meter.firmware_and_revision_code
    expected = "4.3,67"
    assert value == expected, f"Expected '{expected}', got '{value}'"
