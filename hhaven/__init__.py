"""
A well documented and typed API wrapper for https://hentaihaven.xxx.

Documentation: https://hhaven.nekolab.app

Source Code: https://github.com/jokelbaf/hhaven
"""

from . import models, exceptions
from .client import Client

__all__ = [
    "Client",
    "models", 
    "exceptions"
]

__version__ = "0.2.0"
