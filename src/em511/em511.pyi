from decimal import Decimal

from pymodbus.client import ModbusSerialClient

class Em511:
    EM511_REGISTER_RESET_TOT_ENERGY_AND_RUN_HOUR_COUNTER: int
    EM511_REGISTER_RESET_PARTIAL_ENERGY_AND_HOUR_COUNTER: int
    EM511_REGISTER_RESET_DMD_AND_DMD_MAX: int
    EM511_REGISTER_RESET_TO_FACTORY_SETTINGS: int

    def __init__(self, device_address: int, client: ModbusSerialClient) -> None: ...
    V: Decimal
    A: Decimal
    W: Decimal
    W_dmd: Decimal
    W_dmd_peak: Decimal
    A_dmd: Decimal
    A_dmd_peak: Decimal
    Hz: Decimal
    kwh_tot: Decimal
    kwh_partial: Decimal
    hour_counter: Decimal
    lifetime_counter: Decimal
    hour_counter_part: Decimal
    password: int
    alarm_status: int
    alarm_mode: int
    alarm_delay: int
    dmd_integration_time: int
    device_id: int
    baud_rate: int
    parity: int
    stop_bit: int
    reply_delay: int
    identification_code: int
    measure_mode: int

    def _unpack(self, registers: list[int], address: int) -> int: ...
    def _write_register(self, address: int, value: int) -> None: ...
    def _read_register(self, register_name: str) -> Decimal | int: ...
    def _read_input_registers(self, address: int, count: int) -> list[int]: ...
    def reset_tot_energy_and_run_hour_counter(self) -> None: ...
    def reset_partial_energy_and_hour_counter(self) -> None: ...
    def reset_dmd_and_dmd_max(self) -> None: ...
    def reset_to_factory_settings(self) -> None: ...
    def firmware_and_revision_code(self) -> str: ...
