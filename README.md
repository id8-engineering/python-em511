[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/id8-engineering/python-em511/badge)](https://scorecard.dev/viewer/?uri=github.com/id8-engineering/python-em511)

## python-em511

python-em511 provides a simple, Pythonic interface for reading and writing data 
from Carlo Gavazzi EM511 series energy meters over Modbus RTU. It builds on top 
of [pymodbus](https://pypi.org/project/pymodbus/).

## Example usage:

```python
from em511 import Em511
from pymodbus.client import ModbusSerialClient

# Configure the Modbus client
client = ModbusSerialClient(
   port="COM3",  # or "/dev/ttyUSB0" on Linux
   baudrate=9600,
   parity="E",
   stopbits=1,
   bytesize=8,
   # datasheet specifies maximum response timeout of 500ms (typical 40ms)
   timeout=0.5,
)

# Device Modbus address
device_address = 1

# Initialize the EM511 driver
meter = Em511(device_address=device_address, client=client)

# Read voltage
voltage = meter.V
print(f"Voltage: {voltage} V")

# Example of writing a password-protected parameter
meter.password = 1234
```

## Report issues

If you run into problems, you can ask for help in our [issue tracker](https://github.com/id8-engineering/python-em511/issues) on GitHub.

## Contributing
See [CONTRIBUTING.MD](https://github.com/id8-engineering/python-em511/blob/main/CONTRIBUTING.MD) and [DEVELOPMENT.MD](https://github.com/id8-engineering/python-em511/blob/main/DEVELOPMENT.MD).
