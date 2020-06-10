"""A Python 3 wrapper library for the New York Times API"""
from .api import NYTAPI
from .__version__ import __version__

__all__ = ["NYTAPI", "__version__"]