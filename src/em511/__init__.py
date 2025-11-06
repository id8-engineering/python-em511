"""Top-level package for the EM511 driver.

Provides the `Em511` class for reading and writing Modbus registers
using Carlo Gavazzi EM511 energy meters.
"""

from importlib.metadata import PackageNotFoundError, version

from .em511 import Em511

__all__ = ["Em511", "__version__"]

try:
    __version__ = version("python-em511")
except PackageNotFoundError:
    __version__ = "0.0.0"
