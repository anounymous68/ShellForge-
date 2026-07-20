"""
Abstract base class for ShellForge payload generators.

Author: Mostafa Tamime
"""

from abc import ABC, abstractmethod


class PayloadGenerator(ABC):
    """Common interface for reverse and bind shell payload generators."""

    @abstractmethod
    def reverse(self, ip: str, port: int) -> str:
        """Generate a reverse shell payload connecting to *ip*:*port*."""

    @abstractmethod
    def bind(self, port: int) -> str:
        """Generate a bind shell payload listening on *port*."""

    @abstractmethod
    def file_extension(self) -> str:
        """Return the preferred file extension for this payload (e.g. '.sh')."""
