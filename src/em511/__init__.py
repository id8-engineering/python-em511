"""Top-level package for the EM511 driver.

Provides the `Em511` class for reading and writing Modbus registers
using Carlo Gavazzi EM511 energy meters.
"""

from .em511 import Em511

__all__ = ["Em511"]
