# ruff: noqa: S101, PLR2004, SLF001
"""Test file for driver."""

from contextlib import nullcontext
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


def test_range_validation() -> None:
    """Test range validation."""
    client = MagicMock()
    meter = Em511(1, client)

    """Test 1: Should not pass due to out of range."""
    for name, spec in Em511._register_specs.items():  # type: ignore[attr-defined]
        if not spec.range or not spec.writable:
            continue

        client.write_register.return_value.isError.return_value = False
        with nullcontext():
            _ = setattr(meter, name, spec.min)

        invalid_value = spec.max + 1
        with pytest.raises(ValueError, match="Invalid value for"):
            setattr(meter, name, invalid_value)

        invalid_value = spec.min - 1
        with pytest.raises(ValueError, match="Invalid value for"):
            setattr(meter, name, invalid_value)


def test_read_input_registers() -> None:
    """Test all input registers."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    meter = Em511(1, client)

    client.read_input_registers.return_value = mock_result

    """Test 1: Should pass."""
    for name, spec in Em511._register_specs.items():  # type: ignore[attr-defined]
        value_test = spec.min + 1
        mock_result.registers = [value_test, 0x0000]
        client.read_input_registers.return_value = mock_result

        value = getattr(meter, name)
        assert value * spec.scale == value_test


def test_set_all_register() -> None:
    """Test set all registers."""
    client = MagicMock()
    mock_result = MagicMock()
    mock_result.isError.return_value = False
    client.write_register.return_value = mock_result

    meter = Em511(1, client)

    for name, spec in Em511._register_specs.items():  # type: ignore[attr-defined]
        if not spec.writable:
            continue

        value = 1
        setattr(meter, name, value)
        client.write_register.assert_called_once_with(address=spec.address, value=1, device_id=1)
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
