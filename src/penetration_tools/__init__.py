"""
Penetration Testing Toolset

A comprehensive, modular penetration testing framework built with modern DevOps practices.
"""

__version__ = "0.1.0"
__author__ = "Security Team"
__email__ = "security@company.com"

from .config import settings
from .core import logger

__all__ = ["settings", "logger"] 